import pandas as pd

from src.pipeline import enrich_product


INPUT = (
    "data/raw/"
    "Unihack_ Sample Dataset - Input.csv"
)


def test_real_catalogue_pipeline(monkeypatch):

    df = pd.read_csv(INPUT)

    row = df.iloc[0]

    # Prevent the automated test suite from consuming
    # Gemini API quota.
    def fake_attribute_enrichment(text):

        return {
            "raw": {
                "product_type": None,
                "brand": None,
                "series": None,
                "model": None,
                "diameter": None,
                "thickness": None,
                "arbor": None,
                "length": None,
                "width": None,
                "height": None,
                "grit": None,
                "abrasive_grade": None,
                "material": None,
                "application": None,
                "pack_quantity": None,
                "unit_of_measure": None,
                "technology": None,
            },
            "normalized": {
                "product_type": None,
                "brand": None,
                "series": None,
                "model": None,
                "diameter": None,
                "thickness": None,
                "arbor": None,
                "length": None,
                "width": None,
                "height": None,
                "grit": None,
                "abrasive_grade": None,
                "material": None,
                "application": None,
                "pack_quantity": None,
                "unit_of_measure": None,
                "technology": None,
            },
        }

    monkeypatch.setattr(
        "src.pipeline.AttributeEnricher.enrich",
        lambda self, text: fake_attribute_enrichment(text)
    )

    result = enrich_product(row)

    print("\n=== REAL CATALOGUE PIPELINE ===")
    print("Identity:")
    print(result["identity"])

    print("\nBrand:")
    print(result["brand_detection"])

    print("\nManufacturer:")
    print(result["manufacturer_resolution"])

    print("\nAttributes:")
    print(result["attributes"])

    assert result["identity"]["mpn"]
    assert "attributes" in result