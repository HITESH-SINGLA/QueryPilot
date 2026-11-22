from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.ingestion import loader
from backend.app.retrieval.vector_store import VectorStore
from backend.app.ingestion.loader import PDFLoader

class DocumentIngestor:

    def __init__(self, vector_store: VectorStore):

        self.vector_store = vector_store

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def ingest(self, pdf_path: str):

        pages = PDFLoader(pdf_path).load()

        documents = []

        for page in pages:

            chunks = self.splitter.split_text(page.text)

            for chunk in chunks:

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "page": page.page_number,
                            "source": pdf_path,
                        },
                    )
                )

        self.vector_store.add_documents(documents)

        print(f"Indexed {len(documents)} chunks.")