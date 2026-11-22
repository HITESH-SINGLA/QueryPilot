from backend.app.ingestion.loader import PDFLoader


def test_pdf_loader():

    loader = PDFLoader("data/books/sample.pdf")

    pages = loader.load()

    assert len(pages) > 0

    assert pages[0].page_number == 1

    assert isinstance(pages[0].text, str)