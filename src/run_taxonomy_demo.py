import pandas as pd
from pathlib import Path
from src.taxonomy import classify_description

INPUT_FILE = "Unihack_ Sample Dataset - Input.csv"

def main():
    # Look in data/raw first
    path = Path(f"data/raw/{INPUT_FILE}")
    if not path.exists():
        path = Path(f"src/data/raw/{INPUT_FILE}")  # optional fallback

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    # Load CSV
    df = pd.read_csv(path)

    # Clean column names
    df.columns = [str(column).strip() for column in df.columns]

    # Apply taxonomy classification
    classifications = df["Part_Desc"].apply(classify_description)
    df["taxonomy"] = classifications.apply(lambda x: x["taxonomy"])
    df["taxonomy_confidence"] = classifications.apply(lambda x: x["taxonomy_confidence"])

    # Print results
    print("=" * 70)
    print("BATCH 5 — TAXONOMY DEMO")
    print("=" * 70)
    print("\nROWS:", len(df))
    print("\nTAXONOMY COUNTS:")
    print(df["taxonomy"].value_counts(dropna=False))
    print("\nFIRST 10 PRODUCTS:")
    print(df[["Mfg_Part_Num", "Part_Desc", "taxonomy", "taxonomy_confidence"]]
          .head(10)
          .to_string(index=False))

if __name__ == "__main__":
    main()
