import os
import pandas as pd

from .catalogue import enrich_catalogue 

test_input = "data/output/batch4_test_10.csv"
INPUT = "data/raw/Unihack_ Sample Dataset - Input.csv"
OUTPUT = "data/output/enriched_products.csv"

df = pd.read_csv(INPUT).head(10)
df.to_csv(test_input, index=False)



def main():

    os.makedirs("data/output", exist_ok=True)

    print("=" * 80)
    print("BATCH 4 — REAL CATALOGUE ENRICHMENT")
    print("=" * 80)

    print(f"Input : {test_input}")
    print(f"Output: {OUTPUT}")
    print()

    result = enrich_catalogue(test_input)

    result.to_csv(OUTPUT, index=False)

    print()
    print("=" * 80)
    print("CATALOGUE SUMMARY")
    print("=" * 80)

    print(f"Total products: {len(result)}")

    if "status" in result.columns:

        print("\nStatus counts:")
        print(
            result["status"]
            .value_counts(dropna=False)
            .to_string()
        )

    print("\nEvidence counts:")

    if "evidence_count" in result.columns:

        print(
            result["evidence_count"]
            .value_counts()
            .sort_index()
            .to_string()
        )

    print("\nFirst 10 products:")

    columns = [
        "Mfg_Part_Num",
        "Part_Desc",
        "status",
        "evidence_count",
    ]

    available = [
        column
        for column in columns
        if column in result.columns
    ]

    print(
        result[available]
        .head(10)
        .to_string(index=False)
    )

    if "error" in result.columns:

        errors = result[
            result["error"].notna()
        ]

        if len(errors) > 0:

            print()
            print("=" * 80)
            print("FIRST ERRORS")
            print("=" * 80)

            print(
                errors[
                    [
                        "Mfg_Part_Num",
                        "error",
                    ]
                ]
                .head(10)
                .to_string(index=False)
            )

    print()
    print("=" * 80)
    print(f"Saved: {OUTPUT}")
    print("=" * 80)


if __name__ == "__main__":
    main()
