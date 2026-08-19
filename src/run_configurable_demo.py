import pandas as pd

from src.lov_profile import load_lov_profile
from src.lov_engine import LOVEngine


LOV_FILE = "data/demo/company_lov.csv"


PRODUCTS = [
    "4-1/2 inch Steel Cut Off Disc",
    "5 inch Aluminum Cut-Off Disc",
    "Professional Stainless Steel Dishwasher",
    "Unknown Generic Product",
]


def main():

    print("=" * 70)
    print("CONFIGURABLE PRODUCT INTELLIGENCE DEMO")
    print("=" * 70)

    profile = load_lov_profile(
        LOV_FILE
    )

    engine = LOVEngine(
        profile
    )

    print("\nPROFILE")
    print(
        profile.summary()
    )

    print("\nCLASSIFICATION")

    for product in PRODUCTS:

        result = engine.classify(
            product
        )

        print(
            f"\nPRODUCT: {product}"
        )

        print(
            f"CATEGORY: {result['category']}"
        )

        print(
            f"CONFIDENCE: {result['confidence']}"
        )

        print(
            f"SOURCE: {result['source']}"
        )

    print("\nATTRIBUTE NORMALIZATION")

    examples = [
        (
            "Material",
            "steel",
        ),
        (
            "Material",
            "Stainless Steel",
        ),
        (
            "Material",
            "Titanium",
        ),
    ]

    for attribute, value in examples:

        result = engine.normalize_attribute(
            attribute,
            value,
        )

        print(
            f"{attribute} = {value}"
        )

        print(
            result
        )


if __name__ == "__main__":
    main()