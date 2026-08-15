from unittest import result

import pandas as pd

from .pipeline import enrich_product


INPUT = (
    "data/raw/"
    "Unihack_ Sample Dataset - Input.csv"
)


def main():

    df = pd.read_csv(INPUT)

    # Use representative products for the first demo.
    indices = [0, 1, 7]

    for index in indices:

        row = df.iloc[index]

        result = enrich_product(row)

        print("\n")
        print("=" * 80)
        print("PRODUCT ENRICHMENT")
        print("=" * 80)

        print("\nRAW PRODUCT")
        print("-" * 80)
        print("MPN:", row["Mfg_Part_Num"])
        print("Description:", row["Part_Desc"])
        print("Manufacturer:", row["Part_Manuf"])

        print("\nIDENTITY")
        print("-" * 80)
        print(result["identity"])

        print("\nBRAND")
        print("-" * 80)
        print(result["brand_detection"])

        print("\nMANUFACTURER RESOLUTION")
        print("-" * 80)
        print(result["manufacturer_resolution"])

        print("\nCANONICAL IDENTITY")
        print("-" * 80)
        print(result["canonical_identity"])  

        print("\nATTRIBUTES")
        print("-" * 80)

        print(result["attributes"]["normalized"])