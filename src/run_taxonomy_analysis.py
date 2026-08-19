import pandas as pd

INPUT_FILE = "data/raw/Unihack_ Sample Dataset - Input.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 70)
    print("BATCH 5 — TAXONOMY COVERAGE ANALYSIS")
    print("=" * 70)

    print(f"\nTOTAL ROWS: {len(df)}")

    if "taxonomy" not in df.columns:
        from src.taxonomy import classify_dataframe
        df = classify_dataframe(df)

    classified = df["taxonomy"].notna().sum()
    unresolved = df["taxonomy"].isna().sum()

    print(f"CLASSIFIED: {classified}")
    print(f"UNRESOLVED: {unresolved}")

    print("\nTAXONOMY COVERAGE:")
    print(
        df["taxonomy"]
        .fillna("<unresolved>")
        .value_counts()
        .to_string()
    )

    unresolved_df = df[df["taxonomy"].isna()]

    print("\nUNRESOLVED DESCRIPTION SAMPLES:")

    columns = [
        column
        for column in [
            "Mfg_Part_Num",
            "Part_Desc",
            "taxonomy",
            "taxonomy_confidence",
        ]
        if column in unresolved_df.columns
    ]

    print(
        unresolved_df[columns]
        .head(30)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()