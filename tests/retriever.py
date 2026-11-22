from langchain_core.documents import Document

from backend.app.retrieval.vector_store import VectorStore
from backend.app.retrieval.retriever import Retriever


def test_retriever():

    # Create vector store
    vector_store = VectorStore()

    # Add sample documents
    documents = [
        Document(page_content="Time and Work"),
        Document(page_content="Probability"),
        Document(page_content="Geometry"),
    ]

    vector_store.add_documents(documents)

    # Create retriever
    retriever = Retriever(vector_store)

    # Retrieve
    results = retriever.retrieve(
        query="Time and Work",
        top_k=2
    )

    # Print results
    print("\nRetrieved Documents\n")

    for index, document in enumerate(results, start=1):
        print(f"{index}. {document.page_content}")

    # Assertions
    assert len(results) == 2

    assert any(
        "Time and Work" in document.page_content
        for document in results
    )