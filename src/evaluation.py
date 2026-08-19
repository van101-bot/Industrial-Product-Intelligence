from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

EXPECTED_FILE = BASE_DIR / "data" / "raw" / "Unihack_ Expected Output - Delivery Format.csv"
ACTUAL_FILE = BASE_DIR / "data" / "output" / "final_delivery_format.csv"

# ------------------------------------------------------------
# FILE LOADING
# ------------------------------------------------------------

def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path, dtype=str)

# ------------------------------------------------------------
# NORMALISATION
# ------------------------------------------------------------

def normalize_value(value):
    if pd.isna(value):
        return ""
    value = str(value).strip().upper()
    if value.startswith("SKU - "):
        value = value.replace("SKU - ", "")
    if value.startswith("SKU-"):
        value = value.replace("SKU-", "")
    if value in {"NAN", "NONE", "NULL", "<NA>"}:
        return ""
    return value

# ------------------------------------------------------------
# IDENTIFIER ALIGNMENT
# ------------------------------------------------------------

EXPECTED_ID_COLUMNS = [
    "PART_NUMBER",
    "SKU - MY_PART_NUMBER",
    "Mfg_Part_Num",
    "Part_Desc",
    "Part_Manuf",
    "MANUFACTURER_PART_NUMBER",
    "ALTERNATE_PART_NUMBER",
]

ACTUAL_ID_COLUMNS = [
    "PART_NUMBER",
    "SKU - MY_PART_NUMBER",
    "Mfg_Part_Num",
    "Part_Desc",
    "Part_Manuf",
    "MANUFACTURER_PART_NUMBER",
    "ALTERNATE_PART_NUMBER",
]

def find_identifier_column(df, candidates):
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None

def align_dataframes(expected, actual):
    expected_id = find_identifier_column(expected, EXPECTED_ID_COLUMNS)
    actual_id = find_identifier_column(actual, ACTUAL_ID_COLUMNS)

    if expected_id is None:
        raise ValueError("Could not find a usable identifier in expected output.")
    if actual_id is None:
        raise ValueError("Could not find a usable identifier in actual output.")

    expected = expected.copy()
    actual = actual.copy()

    expected["_eval_id"] = expected[expected_id].map(normalize_value)
    actual["_eval_id"] = actual[actual_id].map(normalize_value)

    expected = expected[expected["_eval_id"] != ""].copy()
    actual = actual[actual["_eval_id"] != ""].copy()

    print(f"\nUsing expected_id column: {expected_id}")
    print(f"Using actual_id column: {actual_id}")
    print("Expected IDs sample:", expected["_eval_id"].head(20).tolist())
    print("Actual IDs sample:", actual["_eval_id"].head(20).tolist())

    common_ids = set(expected["_eval_id"]) & set(actual["_eval_id"])
    print("Number of overlapping IDs:", len(common_ids))

    if not common_ids:
        print("⚠️ No overlapping product identifiers found. Continuing with empty alignment.")
        return expected.head(0), actual.head(0), expected_id, actual_id

    expected = expected[expected["_eval_id"].isin(common_ids)].drop_duplicates("_eval_id")
    actual = actual[actual["_eval_id"].isin(common_ids)].drop_duplicates("_eval_id")

    expected = expected.set_index("_eval_id")
    actual = actual.set_index("_eval_id")

    common_ids = sorted(set(expected.index) & set(actual.index))
    expected = expected.loc[common_ids]
    actual = actual.loc[common_ids]

    return expected, actual, expected_id, actual_id

# ------------------------------------------------------------
# EVALUATION
# ------------------------------------------------------------

def evaluate():
    expected = load_csv(EXPECTED_FILE)
    actual = load_csv(ACTUAL_FILE)

    print("=" * 70)
    print("UNIHACK FIELD-LEVEL EVALUATION")
    print("=" * 70)
    print("\nEXPECTED:", expected.shape)
    print("\nACTUAL:", actual.shape)

    expected_aligned, actual_aligned, expected_id, actual_id = align_dataframes(expected, actual)

    print("\nIDENTIFIER ALIGNMENT")
    print("Expected column:", expected_id)
    print("Actual column:", actual_id)
    print("Matched products:", len(expected_aligned))

    return {
        "expected_rows": len(expected),
        "actual_rows": len(actual),
        "matched_products": len(expected_aligned),
    }

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    report = evaluate()
    print("\nEVALUATION COMPLETE")
    print("=" * 70)
    print("Matched products:", report["matched_products"])
    print("Actual output rows:", report["actual_rows"])
    print("Expected output rows:", report["expected_rows"])

if __name__ == "__main__":
    main()
