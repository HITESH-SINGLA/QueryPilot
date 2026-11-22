from backend.app.retrieval.answer_generator import AnswerGenerator
from backend.app.retrieval.web_retriever import WebRetriever


def test_web_retriever():

    retriever = WebRetriever(
        answer_generator=AnswerGenerator()
    )

    answer = retriever.invoke(
        "Who won Wimbledon 2026?"
    )
    
    print(str(answer))
    assert isinstance(answer, str)

    assert len(answer) > 0