from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "raw"


INPUT_FILE = DATA_DIR / "Unihack_ Sample Dataset - Input.csv"
EXPECTED_OUTPUT_FILE = DATA_DIR / "Unihack_ Expected Output - Delivery Format.csv"


def load_input_data() -> pd.DataFrame:
    """Load the 1,000 raw product records."""
    return pd.read_csv(INPUT_FILE)


def load_expected_output() -> pd.DataFrame:
    """Load the provided expected-output examples."""
    return pd.read_csv(EXPECTED_OUTPUT_FILE)


if __name__ == "__main__":
    input_df = load_input_data()
    output_df = load_expected_output()

    print("=== INPUT DATA ===")
    print("Rows:", len(input_df))
    print("Columns:", len(input_df.columns))
    print("Columns:", input_df.columns.tolist())

    print("\n=== EXPECTED OUTPUT ===")
    print("Rows:", len(output_df))
    print("Columns:", len(output_df.columns))