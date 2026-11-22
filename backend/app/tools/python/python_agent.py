import os
import traceback
from pathlib import Path

from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_ollama import ChatOllama

from backend.app.models.python_response import PythonResponse
from backend.app.retrieval.retriever import Retriever
from backend.app.tools.python.python_context_builder import (
    PythonContextBuilder,
)

load_dotenv()

MAX_REPAIR_ATTEMPTS = 3


class PythonAgent:
    """
    Executes Python-based tasks by generating Python code
    and automatically repairing it if execution fails.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: PythonContextBuilder,
    ):

        self.retriever = retriever
        self.context_builder = context_builder

        self.llm = ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:latest",
            ),
            temperature=0,
        )

        self.python = PythonREPLTool()

        # -------------------------------------------------
        # Code Generation Prompt
        # -------------------------------------------------

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an expert Python developer, statistician and data analyst.

Generate executable Python code.

Relevant Context:

{context}

User Request:

{question}

Rules:

- Return ONLY executable Python code.
- Do NOT use markdown.
- Do NOT use triple backticks.
- Do NOT explain anything.
- Always import every required library.
- Never use input().
- Never read from stdin.
- Always print the final answer.
- Never call plt.show().

If a graph is generated:

- import matplotlib.pyplot as plt
- call plt.tight_layout()
- save the graph as output.png

Preferred Libraries:

- numpy
- pandas
- matplotlib.pyplot
- statistics
- scipy.stats (advanced statistics only)
- sklearn

Never use:

- scipy.stats.mean
- scipy.stats.median
- scipy.stats.mode

If context is empty,
solve using only the user request.

If context contains relevant data,
use it.
"""
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

        # -------------------------------------------------
        # Repair Prompt
        # -------------------------------------------------

        self.repair_prompt = ChatPromptTemplate.from_template(
            """
You are an expert Python developer.

The following Python program failed.

{repair_context}

--------------------------------------------------

Repair ONLY the code.

Rules

- Preserve the original intent.
- Fix ONLY the execution error.
- Keep the solution as close as possible.
- Return ONLY executable Python code.
- No markdown.
- No explanations.
- No triple backticks.
- Always import required libraries.
- Always print the final answer.
"""
        )

        self.repair_chain = (
            self.repair_prompt
            | self.llm
            | StrOutputParser()
        )

    # -------------------------------------------------
    # Detect execution failure
    # -------------------------------------------------

    def has_execution_error(
        self,
        result,
    ) -> bool:

        if result is None:
            return False

        result = str(result)

        return (
            "Traceback" in result
            or "Error" in result
            or "Exception" in result
        )
    def invoke(
        self,
        question: str,
        requires_retrieval: bool = False,
        top_k: int = 5,
    ) -> PythonResponse:

        # -------------------------------------------------
        # Clean Previous Artifacts
        # -------------------------------------------------

        for file in (
            "output.png",
            "output.csv",
            "output.xlsx",
            "output.pdf",
        ):

            path = Path(file)

            if path.exists():
                path.unlink()

        # -------------------------------------------------
        # Retrieve Context
        # -------------------------------------------------

        context = ""

        if requires_retrieval:

            documents = self.retriever.retrieve(
                query=question,
                top_k=top_k,
            )

            context = self.context_builder.build_context(
                documents
            )

        print("\n" + "=" * 80)
        print("📚 Retrieved Context")
        print("=" * 80)

        if context:
            print(context)
        else:
            print("No retrieval required.")

        # -------------------------------------------------
        # Initial Code Generation
        # -------------------------------------------------

        code = self.chain.invoke(
            {
                "question": question,
                "context": context,
            }
        )

        print("\n" + "=" * 80)
        print("🐍 Initial Generated Code")
        print("=" * 80)
        print(code)

        result = ""

        # -------------------------------------------------
        # Execute + Repair Loop
        # -------------------------------------------------

        for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):

            print("\n" + "=" * 80)
            print(f"🐍 Execution Attempt {attempt}")
            print("=" * 80)

            try:

                result = self.python.run(code)

            except Exception:

                result = traceback.format_exc()

            print("\nExecution Output")
            print("-" * 80)
            print(result)

            # -------------------------------------------------
            # Success
            # -------------------------------------------------

            if not self.has_execution_error(result):

                print("\n✅ Execution Successful")

                break

            # -------------------------------------------------
            # Failed
            # -------------------------------------------------

            print("\n❌ Execution Failed")

            if attempt == MAX_REPAIR_ATTEMPTS:

                print("\n❌ Maximum repair attempts reached.")

                return PythonResponse(
                    code=code,
                    output=(
                        "I couldn't execute the generated Python "
                        "code after 3 repair attempts.\n"
                        "Please try rephrasing your request."
                    ),
                    artifacts=[],
                    context=context,
                )

            print("\n🔧 Repairing Code...")

            repair_context = (
                self.context_builder.build_repair_context(
                    question=question,
                    context=context,
                    code=code,
                    error=str(result),
                )
            )

            code = self.repair_chain.invoke(
                {
                    "repair_context": repair_context,
                }
            )

            print("\n" + "=" * 80)
            print("🐍 Corrected Code")
            print("=" * 80)
            print(code)

        # -------------------------------------------------
        # Collect Artifacts
        # -------------------------------------------------

        artifacts = []

        for file in (
            "output.png",
            "output.csv",
            "output.xlsx",
            "output.pdf",
        ):

            if Path(file).exists():
                artifacts.append(file)

        print("\n" + "=" * 80)
        print("📦 Generated Artifacts")
        print("=" * 80)

        if artifacts:

            for artifact in artifacts:
                print(artifact)

        else:

            print("No artifacts generated.")

        print("\n" + "=" * 80)
        print("🐍 Final Output")
        print("=" * 80)
        print(result)

        return PythonResponse(
            code=code,
            output=str(result),
            artifacts=artifacts,
            context=context,
        )