from pathlib import Path

import pandas as pd

from .batch_processor import process_dataframe


INPUT = Path(
    "data/raw/Unihack_ Sample Dataset - Input.csv"
)

OUTPUT_DIR = Path("data/output")

OUTPUT = OUTPUT_DIR / "enriched_products.csv"


def main():

    print("=" * 70)
    print("AI PRODUCT ENRICHMENT - BATCH PROCESSOR")
    print("=" * 70)

    print(f"\nInput: {INPUT}")

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_csv(INPUT)

    print(f"Rows loaded: {len(df)}")

    result = process_dataframe(df)

    result.to_csv(
        OUTPUT,
        index=False,
    )

    print("\n" + "=" * 70)
    print("BATCH COMPLETE")
    print("=" * 70)

    print(f"Input rows : {len(df)}")
    print(f"Output rows: {len(result)}")
    print(f"Output file: {OUTPUT}")


if __name__ == "__main__":
    main()