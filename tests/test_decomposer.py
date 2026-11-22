from backend.app.retrieval.decomposer import QuestionDecomposer


def test_decomposer():

    decomposer = QuestionDecomposer()

    questions = decomposer.decompose(
        "Explain Bayes theorem and solve a medical diagnosis example."
    )

    print()

    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q}")

    assert len(questions) >= 2

    assert all(
        isinstance(q, str)
        for q in questions
    )