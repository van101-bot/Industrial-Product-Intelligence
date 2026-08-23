from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DELIVERY_FILE = BASE_DIR / "data" / "output" / "final_delivery_format.csv"
EXPECTED_FILE = BASE_DIR / "data" / "raw" / "Unihack_ Expected Output - Delivery Format.csv"

def validate_delivery():
    print("=" * 70)
    print("FINAL DELIVERY VALIDATION")
    print("=" * 70)

    if not DELIVERY_FILE.exists():
        raise FileNotFoundError(f"Missing delivery file: {DELIVERY_FILE}")

    if not EXPECTED_FILE.exists():
        raise FileNotFoundError(f"Missing expected schema file: {EXPECTED_FILE}")

    actual = pd.read_csv(DELIVERY_FILE, dtype=str, keep_default_na=False)
    expected = pd.read_csv(EXPECTED_FILE, dtype=str, nrows=0)

    print("Output:", DELIVERY_FILE)
    print("Rows:", len(actual))
    print("Columns:", len(actual.columns))

    # Schema checks
    assert list(actual.columns) == list(expected.columns), "Column schema mismatch"
    assert len(actual.columns) == 252, f"Expected 252 columns, got {len(actual.columns)}"
    assert actual.columns.is_unique, "Duplicate columns detected"

    print("Schema: PASS")
    print("252-column delivery format: PASS")

    # Data content checks
    id_columns = ["PART_NUMBER", "Mfg_Part_Num", "Part_Desc"]
    print("\nDATA CONTENT")

    for column in id_columns:
        if column in actual.columns:
            nonempty = actual[column].astype(str).str.strip().ne("").sum()
            print(f"{column}: {nonempty}/{len(actual)} populated")
            if nonempty == 0:
                print(f"WARNING: {column} is completely empty.")

    print("\nFIRST 5 RECORDS")
    preview_columns = [c for c in ["PART_NUMBER", "Mfg_Part_Num", "Part_Desc", "E1_Brand", "Part_Manuf"] if c in actual.columns]
    print(actual[preview_columns].head().to_string(index=False))

    print("\nFINAL STATUS: CHECK COMPLETE")
    return True

if __name__ == "__main__":
    validate_delivery()
