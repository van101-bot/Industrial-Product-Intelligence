from src.attributes import AttributeEnricher


class RealProductExtractor:

    def extract_product_attributes(self, text):

        return {
            "diameter": "4-1/2",
            "thickness": ".045",
            "arbor": "7/8",
            "product_type": "Metal Cut Off Disc",
        }


def test_real_milwaukee_attributes():

    text = (
        '49-94-0107 Milw 4-1/2"x.045"x7/8" '
        'Performance+ Metal Cut Off Disc'
    )

    enricher = AttributeEnricher(
        extractor=RealProductExtractor()
    )

    result = enricher.enrich(text)

    assert result["normalized"]["diameter"] == 4.5
    assert result["normalized"]["thickness"] == 0.045
    assert result["normalized"]["arbor"] == 0.875

    assert (
        result["normalized"]["product_type"]
        == "Metal Cut Off Disc"
    )

    assert result["status"] == "accepted"