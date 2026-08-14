from src.sources.models import SearchResult
from src.sources.ranker import classify_source


def test_manufacturer_source_gets_priority():

    result = SearchResult(
        title="Milwaukee 49-94-0107",
        url="https://www.milwaukeetool.com/product/49-94-0107",
        snippet="Performance+ Metal Cut-Off Disc",
        domain="milwaukeetool.com",
    )

    ranked = classify_source(
        result,
        manufacturer_domain="milwaukeetool.com",
    )

    assert ranked.source_type == "manufacturer"
    assert ranked.score == 1.0


def test_marketplace_is_downgraded():

    result = SearchResult(
        title="Milwaukee 49-94-0107",
        url="https://amazon.com/example",
        snippet="Metal Cut-Off Disc",
        domain="amazon.com",
    )

    ranked = classify_source(
        result,
        manufacturer_domain="milwaukeetool.com",
    )

    assert ranked.source_type == "marketplace"
    assert ranked.score < 0