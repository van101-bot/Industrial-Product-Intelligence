import pandas as pd

from .pipeline import enrich_product


INPUT = (
    "data/raw/"
    "Unihack_ Sample Dataset - Input.csv"
)


class DemoExtractor:

    def extract_product_attributes(self, text):

        return {
            "diameter": "4-1/2",
            "thickness": ".045",
            "arbor": "7/8",
            "product_type": "Metal Cut Off Disc",
        }


class DemoAttributeEnricher:

    def __init__(self):
        self.extractor = DemoExtractor()

    def enrich(self, text):

        from .normalizer import normalize_attribute_record
        from .attribute_evidence import (
            build_attribute_evidence
        )

        raw = self.extractor.extract_product_attributes(text)

        normalized = normalize_attribute_record(raw)

        evidence = build_attribute_evidence(
            raw,
            normalized,
        )

        confidence = {
            key: 0.85
            for key, value in normalized.items()
            if value is not None
        }

        return {
            "raw": raw,
            "normalized": normalized,
            "confidence": confidence,
            "evidence": evidence,
            "status": "accepted",
        }


def main():

    df = pd.read_csv(INPUT)

    row = df.iloc[0]

    result = enrich_product(
        row,
        attribute_enricher=DemoAttributeEnricher(),
    )

    print("=" * 70)
    print("BATCH 3 ATTRIBUTE ENRICHMENT DEMO")
    print("=" * 70)

    print("\nIDENTITY")
    print("-" * 70)
    print(result["identity"])

    print("\nBRAND")
    print("-" * 70)
    print(result["brand"])

    print("\nMANUFACTURER")
    print("-" * 70)
    print(result["manufacturer"])

    print("\nATTRIBUTES")
    print("-" * 70)
    print(result["attributes"])

    print("\nNORMALIZED ATTRIBUTES")
    print("-" * 70)
    print(result["attributes"]["normalized"])

    print("\nEVIDENCE")
    print("-" * 70)

    for item in result["attributes"]["evidence"]:
        print(item)

    print("\nSTATUS")
    print("-" * 70)
    print(result["attributes"]["status"])


if __name__ == "__main__":
    main()