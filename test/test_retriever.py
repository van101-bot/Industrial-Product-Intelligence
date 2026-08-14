from src.retriever import retrieve_page


def test_retrieve_page():

    result = retrieve_page(
        "https://example.com"
    )

    assert result.success is True
    assert result.status_code == 200
    assert "Example Domain" in result.text