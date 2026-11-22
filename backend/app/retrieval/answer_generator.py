import os

from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class AnswerGenerator:
    """
    Generates answers for retrieved documents and
    synthesizes recursive retrieval results.
    """

    def __init__(self):

        self.llm = ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:latest",
            ),
            temperature=0,
        )

        # -------------------------------------------------
        # Prompt for answering a question
        # -------------------------------------------------

        self.answer_prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant.

--------------------------------------------------

Retrieved Context

{context}

--------------------------------------------------

Previous Sub-question Answers

{sub_question_history}

--------------------------------------------------

Current Question

{question}

--------------------------------------------------

Instructions

- Use the retrieved context as the primary source of truth.
- Use previous sub-question answers only if they help answer
  the current question.
- Do NOT use outside knowledge.
- If the answer cannot be found in the retrieved context,
  clearly state that the information is unavailable.
- Keep the answer factual, concise and well-structured.
"""
        )

        self.answer_chain = (
            self.answer_prompt
            | self.llm
            | StrOutputParser()
        )

        # -------------------------------------------------
        # Prompt for synthesizing recursive answers
        # -------------------------------------------------

        self.synthesis_prompt = ChatPromptTemplate.from_template(
            """
You are given answers to multiple sub-questions.

--------------------------------------------------

Original Question

{question}

--------------------------------------------------

Sub-question Answers

{sub_question_history}

--------------------------------------------------

Instructions

- Combine all answers into one coherent response.
- Remove redundant information.
- Preserve important details.
- Produce a natural, well-structured final answer.
"""
        )

        self.synthesis_chain = (
            self.synthesis_prompt
            | self.llm
            | StrOutputParser()
        )

    def generate(
        self,
        question: str,
        documents: list[Document],
        sub_question_history: str = "",
    ) -> str:

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        return self.answer_chain.invoke(
            {
                "question": question,
                "context": context,
                "sub_question_history": sub_question_history,
            }
        )

    def synthesize(
        self,
        question: str,
        sub_question_history: str,
    ) -> str:

        return self.synthesis_chain.invoke(
            {
                "question": question,
                "sub_question_history": sub_question_history,
            }
        )