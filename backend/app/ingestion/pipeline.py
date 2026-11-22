from backend.app.ingestion.loader import PDFLoader
from backend.app.ingestion.cleaner import TextCleaner
from backend.app.ingestion.chunker import TextChunker
from backend.app.retrieval.vector_store import VectorStore

from langchain_core.documents import Document


class IngestionPipeline:
    """
    End-to-end pipeline for indexing a PDF.
    """

    def __init__(self):

        self.loader = PDFLoader
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.vector_store = VectorStore()

    def ingest(self, pdf_path: str):

        loader = self.loader(pdf_path)

        pages = loader.load()

        documents = []

        for page in pages:

            cleaned_text = self.cleaner.clean(page.text)

            chunks = self.chunker.chunk(cleaned_text)

            for chunk in chunks:

                documents.append(
                    Document(
                        page_content=chunk.page_content,
                        metadata={
                            "page": page.page_number,
                            "source": pdf_path
                        }
                    )
                )

        self.vector_store.add_documents(documents)

        return len(documents)