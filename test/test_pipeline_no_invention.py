import pandas as pd

from src.pipeline import enrich_product


class EmptyExtractor:

    def extract_product_attributes(self, text):

        return {
            "diameter": None,
            "thickness": None,
            "arbor": None,
            "product_type": None,
        }


class EmptyAttributeEnricher:

    def enrich(self, text):

        return {
            "raw": {
                "diameter": None,
                "thickness": None,
                "arbor": None,
                "product_type": None,
            },
            "normalized": {
                "diameter": None,
                "thickness": None,
                "arbor": None,
                "product_type": None,
            },
            "confidence": {},
            "evidence": [],
            "status": "needs_review",
        }


def test_pipeline_does_not_invent_attributes():

    input_path = (
        "data/raw/"
        "Unihack_ Sample Dataset - Input.csv"
    )

    df = pd.read_csv(input_path)

    row = df.iloc[0]

    result = enrich_product(
        row,
        attribute_enricher=EmptyAttributeEnricher(),
    )

    attributes = result["attributes"]["normalized"]

    assert attributes["diameter"] is None
    assert attributes["thickness"] is None
    assert attributes["arbor"] is None

    assert result["attributes"]["evidence"] == []

    assert (
        result["attributes"]["status"]
        == "needs_review"
    )