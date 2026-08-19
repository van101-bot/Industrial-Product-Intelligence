import os
import pandas as pd

from src.final_output import flatten_enriched_dataframe


INPUT = "data/output/enriched_products.csv"
OUTPUT = "data/output/final_enriched_products.csv"


def main():

    if not os.path.exists(INPUT):
        raise FileNotFoundError(
            f"Input file not found: {INPUT}"
        )

    df = pd.read_csv(INPUT)

    final_df = flatten_enriched_dataframe(df)

    final_df.to_csv(
        OUTPUT,
        index=False,
    )

    print("=" * 70)
    print("BATCH 5 — FINAL SEARCH-READY OUTPUT")
    print("=" * 70)

    print(f"INPUT ROWS:  {len(df)}")
    print(f"OUTPUT ROWS: {len(final_df)}")

    print("\nCOLUMNS:")
    for column in final_df.columns:
        print(f" - {column}")

    print("\nFIRST 5 PRODUCTS:")
    print(
        final_df.head(5).to_string(index=False)
    )

    print("\nOUTPUT:")
    print(OUTPUT)


if __name__ == "__main__":
    main()