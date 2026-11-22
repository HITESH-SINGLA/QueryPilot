from backend.app.ingestion.chunker import TextChunker

def test_chunk_order_is_preserved():
    """
    Ensure the order of information is preserved after chunking.
    """

    text = """
    First Topic.

    Second Topic.

    Third Topic.
    """

    chunker = TextChunker()
    chunks = chunker.chunk(text)

    reconstructed_text = " ".join(
        chunk.page_content for chunk in chunks
    )

    assert reconstructed_text.index("First Topic") < reconstructed_text.index("Second Topic")
    assert reconstructed_text.index("Second Topic") < reconstructed_text.index("Third Topic")