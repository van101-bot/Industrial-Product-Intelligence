from pathlib import Path
from unittest import result
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

EXPECTED_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "Unihack_ Expected Output - Delivery Format.csv"
)

ACTUAL_FILE = (
    BASE_DIR
    / "data"
    / "output"
    / "final_delivery_format.csv"
)


def normalize(value):
    if pd.isna(value):
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("\n", " ")
        .replace("\r", " ")
    )


def main():

    print("=" * 70)
    print("BATCH 8 — DELIVERY EVALUATION")
    print("=" * 70)

    expected = pd.read_csv(EXPECTED_FILE)
    actual = pd.read_csv(ACTUAL_FILE)

    common = [
        column
        for column in expected.columns
        if column in actual.columns
    ]

    print()
    print("EXPECTED ROWS:", len(expected))
    print("ACTUAL ROWS:", len(actual))

    print("EXPECTED COLUMNS:", len(expected.columns))
    print("ACTUAL COLUMNS:", len(actual.columns))
    print("COMMON COLUMNS:", len(common))

    if not common:
        print()
        print("ERROR: No comparable fields.")
        return

    print()
    print("FIELDS BEING EVALUATED:")

    for column in common:
        print(" -", column)

    # Compare only rows that both files contain.
    rows = min(len(expected), len(actual))

    expected = expected.iloc[:rows]
    actual = actual.iloc[:rows]

    results = []

    for column in common:

        exp = expected[column].map(normalize)
        act = actual[column].map(normalize)

        expected_nonempty = exp != ""

        coverage = (
            expected_nonempty.mean()
            if len(exp)
            else 0
        )

        exact_matches = (
            (exp == act) &
            expected_nonempty
        ).sum()

        comparable = expected_nonempty.sum()

        exact_accuracy = (
            exact_matches / comparable
            if comparable
            else 0
        )

        results.append({
            "field": column,
            "expected_nonempty": int(comparable),
            "actual_nonempty": int((act != "").sum()),
            "coverage": coverage,
            "exact_accuracy": exact_accuracy,
        })

    result_df = pd.DataFrame(results)

    output_file = (
        BASE_DIR
        / "data"
        / "output"
        / "batch8_field_evaluation.csv"
    )

    result_df.to_csv(
        output_file,
        index=False,
    )

    print()
    print("=" * 70)
    print("BATCH 8 RESULTS")
    print("=" * 70)

    print(
        "FIELDS COMPARED:",
        len(result_df)
    )

    print(
        "AVERAGE EXPECTED COVERAGE:",
        round(
            result_df["coverage"].mean() * 100,
            2
        ),
        "%"
    )

    print(
        "AVERAGE EXACT ACCURACY:",
        round(
            result_df["exact_accuracy"].mean() * 100,
            2
        ),
        "%"
    )

    print()
    print("TOP FIELDS:")

    print(
        result_df
        .sort_values(
            "exact_accuracy",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

    print()
    print("REPORT:")
    print(output_file)


if __name__ == "__main__":
    main()

if result["overlap"] == 0:
    print()
    print("=" * 70)
    print("EVALUATION STATUS: NOT EVALUATABLE")
    print("=" * 70)
    print(
        "Expected and actual datasets contain no common PART_NUMBER values."
    )
    print(
        "Exact accuracy must NOT be interpreted as model accuracy."
    )
    print("=" * 70)