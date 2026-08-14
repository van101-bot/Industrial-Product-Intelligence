import pandas as pd

from src.pipeline import enrich_product


INPUT = (
    "data/raw/"
    "Unihack_ Sample Dataset - Input.csv"
)


def test_real_catalogue_pipeline():

    df = pd.read_csv(INPUT)

    row = df.iloc[0]

    result = enrich_product(row)

    print("\n")
    print("=" * 60)
    print("REAL ENRICHMENT PIPELINE")
    print("=" * 60)

    print("\nIDENTITY:")
    print(result["identity"])

    print("\nBRAND DETECTION:")
    print(result["brand_detection"])

    print("\nMANUFACTURER:")
    print(result["manufacturer_resolution"])

    print("\nCANONICAL IDENTITY:")
    print(result["canonical_identity"])

    assert result["identity"]["mpn"]