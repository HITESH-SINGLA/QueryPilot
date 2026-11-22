from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings


class TextChunker:
    """
    Splits text into semantically meaningful chunks using LangChain's
    SemanticChunker.

    Workflow:
    1. Split the input text into sentences.
    2. Generate an embedding for each sentence using a HuggingFace model.
    3. Compute the semantic similarity between consecutive sentences.
    4. Detect topic shifts based on the chosen breakpoint strategy.
    5. Merge semantically related sentences into a single chunk.
    """

    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.chunker = SemanticChunker(
            embeddings=embeddings,
            breakpoint_threshold_type="gradient"
        )

    def chunk(self, text: str):
        """
        Splits the input text into semantic chunks.

        Args:
            text (str): Input text.

        Returns:
            List[Document]: LangChain Document objects containing semantic chunks.
        """
        return self.chunker.create_documents([text])