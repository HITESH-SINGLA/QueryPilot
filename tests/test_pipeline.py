from backend.app.ingestion.pipeline import IngestionPipeline


def test_pipeline():

    pipeline = IngestionPipeline()

    count = pipeline.ingest(
        "data/books/sample.pdf"
    )
	
    assert count > 0

    print(f"\nIndexed {count} chunks successfully.")