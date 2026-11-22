from dataclasses import dataclass


@dataclass
class QueryBundle:
    """
    Represents a query as it flows through the
    Adaptive RAG pipeline.
    """

    # Original user question
    original_query: str

    # Standalone question after resolving conversation references
    standalone_query: str

    # Routing Decision
    strategy: str = ""

    reason: str = ""

    confidence: float = 0.0