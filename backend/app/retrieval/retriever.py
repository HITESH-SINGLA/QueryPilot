from langchain_core.documents import Document

from backend.app.retrieval.vector_store import VectorStore
from backend.app.retrieval.decomposer import QuestionDecomposer


class Retriever:

    def __init__(self, vector_store: VectorStore):

        self.vector_store = vector_store
        self.decomposer = QuestionDecomposer()

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> list[Document]:

        return self.vector_store.similarity_search(
            query=query,
            top_k=top_k
        )
    def retrieve_with_score(
        self,
        query: str,
        top_k: int = 3,
    ):

        return self.vector_store.similarity_search_with_score(
            query=query,
            top_k=top_k,
        )
    def retrieve_decomposed(
        self,
        query: str,
        top_k: int = 5
    ) -> dict:

        sub_questions = self.decomposer.decompose(query)

        results = {}

        for question in sub_questions:

            results[question] = self.retrieve(
                question,
                top_k
            )

        return results