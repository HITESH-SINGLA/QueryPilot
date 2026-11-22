from langchain_core.documents import Document

from backend.app.retrieval.answer_generator import AnswerGenerator


def test_answer_generator():

    generator = AnswerGenerator()

    documents = [
        Document(
            page_content="""
Bayes' Theorem describes the probability of an event based on prior knowledge of related conditions.

Formula:
P(A|B) = P(B|A) * P(A) / P(B)
"""
        )
    ]

    answer = generator.generate(
        question="What is Bayes' Theorem?",
        documents=documents,
        history=""
    )

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0