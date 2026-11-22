import os

from dotenv import load_dotenv

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()


class QuestionDecomposer:
    """
    Decomposes a standalone user question into the minimum number
    of independent sub-questions required to answer it.

    The input question is assumed to already be standalone
    (all pronouns/references have already been resolved).
    """

    def __init__(self):

        self.llm = ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:latest",
            ),
            temperature=0,
            format="json",
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an API.

Your ONLY job is to return valid JSON.

Never return:
- Python code
- Markdown
- Explanations
- Notes
- Examples

Return ONLY a JSON object that follows this schema:

{{
    "questions": [
        "<question1>",
        "<question2>"
    ]
}}

Your task is to split a standalone question into the minimum number
of independent questions required to answer it.

Rules:

- The input question is already standalone.
- Do NOT resolve pronouns.
- Do NOT infer missing information.
- Preserve EVERY part of the user's intent.
- Never omit information.
- Every sub-question must be independently answerable.
- If the question is already atomic, return exactly ONE question.
- Do NOT answer the question.

--------------------------------------------------

Example 1

Input:
Who is the Prime Minister of India and what is the age of the Prime Minister of India?

Output:

{{
    "questions": [
        "Who is the Prime Minister of India?",
        "What is the age of the Prime Minister of India?"
    ]
}}

--------------------------------------------------

Example 2

Input:
What is TCP?

Output:

{{
    "questions": [
        "What is TCP?"
    ]
}}

--------------------------------------------------

Example 3

Input:
Who founded Microsoft and who founded Apple?

Output:

{{
    "questions": [
        "Who founded Microsoft?",
        "Who founded Apple?"
    ]
}}

--------------------------------------------------

Question:

{question}

--------------------------------------------------

Return ONLY valid JSON.
"""
        )

        self.chain = (
            self.prompt
            | self.llm
            | JsonOutputParser()
        )

    def decompose(
        self,
        question: str,
    ) -> list[str]:

        try:

            parsed = self.chain.invoke(
                {
                    "question": question,
                }
            )

            print("\n================ DECOMPOSER ================")
            print(parsed)
            print("============================================\n")

            questions = parsed.get(
                "questions",
                [],
            )

            if not isinstance(
                questions,
                list,
            ):
                raise ValueError(
                    "'questions' must be a list."
                )

            questions = [
                q.strip()
                for q in questions
                if isinstance(q, str) and q.strip()
            ]

            if not questions:
                raise ValueError(
                    "No questions returned."
                )

            print("\n================ SUB QUESTIONS ================")

            for index, sub_question in enumerate(
                questions,
                start=1,
            ):
                print(f"{index}. {sub_question}")

            print("================================================\n")

            return questions

        except Exception as e:

            print(f"Decomposer Error: {e}")

            print("\nFalling back to original question.\n")

            return [question]