from pathlib import Path
import pandas as pd

from src.pipeline import run_pipeline
from src.final_output import build_final_output


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "Unihack_ Sample Dataset - Input.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "output"
    / "final_delivery_format.csv"
)


def main():

    print("=" * 70)
    print("INDUSTRIAL PRODUCT INTELLIGENCE")
    print("PRODUCTION PIPELINE")
    print("=" * 70)

    print(f"\nINPUT : {INPUT_FILE}")
    print(f"OUTPUT: {OUTPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input dataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"\nInput rows: {len(df):,}")

    enriched = run_pipeline(df)

    print(f"Enriched rows: {len(enriched):,}")

    final = build_final_output(enriched)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nFINAL OUTPUT")
    print(f"Rows    : {len(final):,}")
    print(f"Columns : {len(final.columns):,}")
    print(f"File    : {OUTPUT_FILE}")

    print("\nSTATUS: SUCCESS")


if __name__ == "__main__":
    main()