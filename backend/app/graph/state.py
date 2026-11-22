from typing import TypedDict

from backend.app.models.query_bundle import QueryBundle


class RAGState(TypedDict):

    question: str

    query_bundle: QueryBundle | None

    route: str | None

    answer: str | None