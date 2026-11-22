from langchain_core.documents import Document


class PythonContextBuilder:
    """
    Converts retrieved documents into a context string
    for the Python Agent.
    """

    def build_context(
        self,
        documents: list[Document]
    ) -> str:

        if not documents:
            return ""

        return "\n\n".join(
            document.page_content
            for document in documents
        )