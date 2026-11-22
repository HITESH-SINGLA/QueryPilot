from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


class VectorStore:
    """
    Wrapper around ChromaDB.

    Responsible for:
    1. Generating embeddings
    2. Storing documents
    3. Retrieving documents
    """

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.vector_db = Chroma(
            collection_name="adaptive_rag",
            embedding_function=self.embeddings,
            persist_directory="data/chroma"
        )

    def add_documents(self, documents: list[Document]):

        self.vector_db.add_documents(documents)

    def similarity_search(self, query: str, top_k: int = 5):

        return self.vector_db.similarity_search(
            query,
            k=top_k
        )
    def similarity_search_with_score(
        self,
        query: str,
        top_k: int = 3,
    ):

        return self.vector_db.similarity_search_with_score(
            query,
            k=top_k,
        )

    def count(self):

        return self.vector_db._collection.count()