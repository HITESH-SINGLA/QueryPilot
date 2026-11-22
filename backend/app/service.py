from backend.app.ingestion.document_ingestor import DocumentIngestor
from backend.app.memory.conversation_memory import ConversationMemory

from backend.app.retrieval.adaptive_retriever import AdaptiveRetriever
from backend.app.retrieval.answer_generator import AnswerGenerator
from backend.app.retrieval.decomposer import QuestionDecomposer
from backend.app.retrieval.direct_retriever import DirectRetriever
from backend.app.retrieval.query_constructor import QueryConstructor
from backend.app.retrieval.retriever import Retriever
from backend.app.retrieval.router import QueryRouter
from backend.app.retrieval.vector_store import VectorStore
from backend.app.retrieval.web_retriever import WebRetriever

from backend.app.tools.python.python_agent import PythonAgent
from backend.app.tools.python.python_context_builder import (
    PythonContextBuilder,
)

# ==================================================
# Shared Services
# ==================================================

vector_store = VectorStore()

conversation_memory = ConversationMemory()

retriever = Retriever(vector_store)

document_ingestor = DocumentIngestor(vector_store)

answer_generator = AnswerGenerator()

decomposer = QuestionDecomposer()

query_constructor = QueryConstructor(
    conversation_memory=conversation_memory,
)

router = QueryRouter()

python_context_builder = PythonContextBuilder()

# ==================================================
# Retrieval Strategies
# ==================================================

direct_retriever = DirectRetriever(
    retriever=retriever,
    answer_generator=answer_generator,
)

web_retriever = WebRetriever(
    answer_generator=answer_generator,
)

# ==================================================
# Python Agent
# ==================================================

python_agent = PythonAgent(
    retriever=retriever,
    context_builder=python_context_builder,
)

# ==================================================
# Adaptive RAG
# ==================================================

adaptive_retriever = AdaptiveRetriever(
    query_constructor=query_constructor,
    decomposer=decomposer,
    router=router,
    direct_retriever=direct_retriever,
    web_retriever=web_retriever,
    python_agent=python_agent,
	answer_generator=answer_generator,
)