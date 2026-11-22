import os

from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


class GeneralChat:
    """
    Handles general conversational queries
    that do not require document retrieval.
    """

    def __init__(self):

        self.llm = ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:latest"
            ),
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant.

Answer the user's question as accurately as possible.

If you are unsure or if the question requires
recent information from the internet, simply reply:

WEB_SEARCH

Question:
{question}
"""
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def invoke(
        self,
        question: str
    ) -> str:

        return self.chain.invoke(
            {
                "question": question
            }
        )