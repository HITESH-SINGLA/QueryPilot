from backend.app.models.query_bundle import QueryBundle
from backend.app.retrieval.router import QueryRouter


def test_router():

    router = QueryRouter()

    bundle = QueryBundle(
        original_query="Plot my percentile trend",
        standalone_query="Plot my percentile trend",
    )

    routed = router.route(
        query_bundle=bundle,
        uploaded_files=[
            "mock_scores.pdf"
        ]
    )

    assert routed.route in [
        "DIRECT",
        "RECURSIVE",
        "WEB",
        "PYTHON"
    ]