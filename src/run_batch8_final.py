from pathlib import Path
import pandas as pd

from src.pipeline import run_pipeline
from src.final_output import build_delivery_output


INPUT = Path(
    "data/raw/Unihack_ Sample Dataset - Input.csv"
)

OUTPUT = Path(
    "data/output/batch8_final_delivery.csv"
)


def main():

    print("=" * 70)
    print("BATCH 8 — FINAL DELIVERY PIPELINE")
    print("=" * 70)

    df = pd.read_csv(INPUT)

    print("INPUT:", len(df))

    enriched = run_pipeline(df)

    delivery = build_delivery_output(enriched)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    delivery.to_csv(
        OUTPUT,
        index=False,
    )

    print("OUTPUT:", len(delivery))
    print("COLUMNS:", len(delivery.columns))
    print("FILE:", OUTPUT)

    assert len(delivery) == len(df)
    assert len(delivery.columns) == 252

    assert "PART_NUMBER" in delivery.columns
    assert "Mfg_Part_Num" in delivery.columns
    assert "Part_Desc" in delivery.columns

    print()
    print("SCHEMA: PASS")
    print("ROW COUNT: PASS")
    print("BATCH 8: PASS")


if __name__ == "__main__":
    main()