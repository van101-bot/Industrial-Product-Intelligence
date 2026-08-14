from src.sources.models import SearchResult
from src.sources.search import MockSearchProvider


def test_search_provider_returns_results():

    results = [
        SearchResult(
            title="Milwaukee 49-94-0107",
            url="https://www.milwaukeetool.com/example",
            snippet="Performance+ Metal Cut-Off Disc",
            domain="milwaukeetool.com",
        ),
        SearchResult(
            title="Example distributor",
            url="https://example.com/product",
            snippet="Milwaukee cutting disc",
            domain="example.com",
        ),
    ]

    provider = MockSearchProvider(results)

    output = provider.search(
        "49-94-0107 Milwaukee",
        max_results=1,
    )

    assert len(output) == 1
    assert output[0].domain == "milwaukeetool.com"