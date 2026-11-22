from langchain_core.documents import Document


class PythonContextBuilder:
    """
    Builds context for the Python Agent.
    """

    def build_context(
        self,
        documents: list[Document],
    ) -> str:

        if not documents:
            return ""

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    def build_repair_context(
        self,
        question: str,
        context: str,
        code: str,
        error: str,
    ) -> str:

        return f"""
The following Python program failed during execution.

==================================================

User Request

{question}

==================================================

Retrieved Context

{context if context else "No retrieved context."}

==================================================

Previously Generated Code

{code}

==================================================

Execution Error

{error}

==================================================

Fix ONLY the execution error.

Do not change the original intent.

Return ONLY executable Python code.
"""