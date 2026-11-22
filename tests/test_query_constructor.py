from backend.app.retrieval.query_constructor import QueryConstructor


def test_query_constructor():

    constructor = QueryConstructor()

    bundle = constructor.construct(
        "Explain Bayes theorem."
    )

    assert bundle.original_query != ""

    assert bundle.standalone_query != ""

    assert isinstance(bundle.alternate_queries, list)