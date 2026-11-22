from langchain_core.documents import Document

from backend.app.retrieval.vector_store import VectorStore


def test_vector_store():

    store = VectorStore()

    documents = [

        Document(
            page_content="Time and Work"
        ),

        Document(
            page_content="Probability"
        ),

        Document(
            page_content="Geometry"
        )

    ]

    store.add_documents(documents)

    print("\nTotal Indexed Documents :", store.count())

    results = store.similarity_search(
        "Work and Time",
        k=2
    )

    print("\nRetrieved Documents\n")

    for doc in results:

        print(doc.page_content)

    assert len(results) == 2

    assert any(
        "Time" in doc.page_content
        for doc in results
    )