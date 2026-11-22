import os

from dotenv import load_dotenv
from tavily import TavilyClient

from langchain_core.documents import Document

from backend.app.retrieval.answer_generator import AnswerGenerator

load_dotenv()


class WebRetriever:
    """
    Retrieves information from the web and generates
    an answer using the retrieved web documents.
    """

    def __init__(
        self,
        answer_generator: AnswerGenerator,
    ):

        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

        self.answer_generator = answer_generator

    def invoke(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        try:

            response = self.client.search(
                query=question,
                max_results=top_k,
            )

        except Exception as e:

            print(f"Web Search Error: {e}")

            return "Unable to retrieve information from the web."

        print("\n" + "=" * 80)
        print("🌐 Web Search Results")
        print("=" * 80)

        documents = []

        for index, result in enumerate(response["results"], start=1):

            print(f"\nResult {index}")
            print("-" * 80)
            print(f"Title  : {result.get('title', '')}")
            print(f"URL    : {result.get('url', '')}")
            print(f"Content:\n{result.get('content', '')}")

            documents.append(
                Document(
                    page_content=result.get(
                        "content",
                        "",
                    ),
                    metadata={
                        "title": result.get(
                            "title",
                            "",
                        ),
                        "source": result.get(
                            "url",
                            "",
                        ),
                    },
                )
            )

        print("=" * 80)

        answer = self.answer_generator.generate(
            question=question,
            documents=documents,
        )

        print("\n🤖 Generated Answer")
        print("-" * 80)
        print(answer)
        print("=" * 80)

        return answer