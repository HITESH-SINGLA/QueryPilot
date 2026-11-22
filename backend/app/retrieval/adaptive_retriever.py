from backend.app.strategies import (
    DIRECT_RAG,
    PYTHON,
)

from backend.app.retrieval.direct_retriever import DirectRetriever
from backend.app.retrieval.query_constructor import QueryConstructor
from backend.app.retrieval.router import QueryRouter
from backend.app.retrieval.web_retriever import WebRetriever
from backend.app.tools.python.python_agent import PythonAgent
from backend.app.retrieval.decomposer import QuestionDecomposer
from backend.app.retrieval.answer_generator import AnswerGenerator
from backend.app.models.query_bundle import QueryBundle

SIMILARITY_THRESHOLD = 0.6


class AdaptiveRetriever:
    """
    Coordinates the Adaptive RAG pipeline.

    Responsibilities:
    1. Construct a standalone query.
    2. Select the reasoning strategy.
    3. Decide between local retrieval and web search.
    4. Execute the selected strategy.
    5. Persist the conversation.
    """

    def __init__(
        self,
        query_constructor: QueryConstructor,
        decomposer: QuestionDecomposer,
        router: QueryRouter,
        direct_retriever: DirectRetriever,
        web_retriever: WebRetriever,
        python_agent: PythonAgent,
        answer_generator: AnswerGenerator,
    ):

        self.query_constructor = query_constructor
        self.decomposer = decomposer
        self.router = router
        self.direct_retriever = direct_retriever
        self.web_retriever = web_retriever
        self.python_agent = python_agent
        self.answer_generator = answer_generator

    def should_use_local(
        self,
        query: str,
    ) -> bool:

        print("\n🔍 Checking Vector Similarity")

        results = self.direct_retriever.retriever.retrieve_with_score(
            query=query,
            top_k=3,
        )

        if not results:

            print("No matching documents found.")

            return False

        print("\n================ VECTOR SEARCH ================")

        for index, (_, distance) in enumerate(results, start=1):
            print(f"Result {index} Distance : {distance:.4f}")

        best_distance = min(
            distance
            for _, distance in results
        )

        decision = (
            "LOCAL"
            if best_distance <= SIMILARITY_THRESHOLD
            else "WEB"
        )

        print(f"\nBest Distance : {best_distance:.4f}")
        print(f"Decision      : {decision}")
        print("===============================================\n")

        return best_distance <= SIMILARITY_THRESHOLD

    def execute_question(
        self,
        question: str,
        strategy: str,
        top_k: int = 5,
    ):

        if strategy == PYTHON:

            print("\n🐍 Executing Python Agent")

            return self.python_agent.invoke(
                question=question,
                top_k=top_k,
            )

        if strategy == DIRECT_RAG:

            if self.should_use_local(question):

                print("\n🟢 Using Local Retrieval")

                return self.direct_retriever.invoke(
                    question=question,
                    top_k=top_k,
                )

            print("\n🌐 Using Web Search")

            return self.web_retriever.invoke(
                question=question,
            )

        raise ValueError(
            f"Unsupported strategy: {strategy}"
        )
    def save_conversation(
        self,
        question: str,
        answer,
    ):

        memory = self.query_constructor.conversation_memory

        memory.add_user_message(question)

        if isinstance(answer, str):

            assistant_message = answer

        elif hasattr(answer, "output"):

            assistant_message = (
                answer.output.strip()
                if answer.output.strip()
                else "Python code executed successfully."
            )

        else:

            assistant_message = str(answer)

        memory.add_assistant_message(
            assistant_message
        )

    def invoke(
        self,
        question: str,
        uploaded_files: list[str] | None = None,
        top_k: int = 5,
    ):

        uploaded_files = uploaded_files or []

        print("\n" + "=" * 80)
        print("🚀 Adaptive RAG Pipeline")
        print("=" * 80)

        print("\n📝 Original Question")
        print(question)

        # --------------------------------------------------
        # Step 1 : Query Construction
        # --------------------------------------------------

        bundle = self.query_constructor.construct(
            question=question,
        )

        print("\n🔹 Standalone Query")
        print(bundle.standalone_query)

        # --------------------------------------------------
        # Step 2 : Route ONCE
        # --------------------------------------------------

        bundle = self.router.route(bundle)

        print("\n🔹 Execution Plan")
        print(f"Strategy   : {bundle.strategy}")
        print(f"Reason     : {bundle.reason}")
        print(f"Confidence : {bundle.confidence:.2f}")

        # ==================================================
        # PYTHON
        # ==================================================

        if bundle.strategy == PYTHON:

            answer = self.execute_question(
                question=bundle.standalone_query,
                strategy=PYTHON,
                top_k=top_k,
            )

            self.save_conversation(
                question=bundle.original_query,
                answer=answer,
            )

            return answer

        # ==================================================
        # DIRECT RAG
        # ==================================================

        sub_questions = self.decomposer.decompose(
            bundle.standalone_query,
        )

        print("\n🔹 Sub Questions")

        for index, sub_question in enumerate(
            sub_questions,
            start=1,
        ):
            print(f"{index}. {sub_question}")

        history = []

        for index, sub_question in enumerate(
            sub_questions,
            start=1,
        ):

            print("\n" + "=" * 80)
            print(f"🔍 Solving Sub-question {index}")
            print("=" * 80)

            answer = self.execute_question(
                question=sub_question,
                strategy=DIRECT_RAG,
                top_k=top_k,
            )

            if hasattr(answer, "output"):
                answer_text = answer.output
            else:
                answer_text = str(answer)

            history.append(
                {
                    "question": sub_question,
                    "answer": answer_text,
                }
            )

        # --------------------------------------------------
        # Final Answer
        # --------------------------------------------------

        if len(history) == 1:

            final_answer = history[0]["answer"]

        else:

            sub_question_history = "\n\n".join(
                f"Question: {item['question']}\n"
                f"Answer: {item['answer']}"
                for item in history
            )

            final_answer = self.answer_generator.synthesize(
                question=bundle.original_query,
                sub_question_history=sub_question_history,
            )

        self.save_conversation(
            question=bundle.original_query,
            answer=final_answer,
        )

        return final_answer