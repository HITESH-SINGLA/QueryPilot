from backend.app.retrieval.answer_generator import AnswerGenerator
from backend.app.retrieval.retriever import Retriever


class DirectRetriever:
    """
    Handles simple queries by retrieving relevant documents
    and generating an answer directly.
    """

    def __init__(
        self,
        retriever: Retriever,
        answer_generator: AnswerGenerator,
    ):

        self.retriever = retriever
        self.answer_generator = answer_generator

    def invoke(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        documents = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        print("\n" + "=" * 80)
        print("📚 Retrieved Documents")
        print("=" * 80)

        print(f"Total Retrieved Chunks: {len(documents)}")

        for index, document in enumerate(documents, start=1):

            print(f"\nChunk {index}")
            print("-" * 80)

            if document.metadata:
                print("Metadata:")
                print(document.metadata)
                print()

            print(document.page_content[:500])
            print()

        print("=" * 80)

        # ----------------------------------------
        # Generate Answer
        # ----------------------------------------

        answer = self.answer_generator.generate(
            question=question,
            documents=documents,
        )

        print("\n🤖 Generated Answer")
        print("-" * 80)
        print(answer)
        print("=" * 80)

        return answer