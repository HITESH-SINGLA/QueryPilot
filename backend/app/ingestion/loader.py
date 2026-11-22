from pathlib import Path

import fitz

from backend.app.models.page import Page


class PDFLoader:

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

    def load(self) -> list[Page]:

        document = fitz.open(self.pdf_path)

        pages = []

        for page_number, page in enumerate(document):

            pages.append(
                Page(
                    page_number=page_number + 1,
                    text=page.get_text()
                )
            )

        document.close()

        return pages

# We didn't use load_pdf() because in future we have plan to implement a common functionality for .txt, .docx, .pdf, etc. So we can use this class to load pdf