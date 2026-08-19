import pandas as pd


EXPECTED = (
    "data/raw/"
    "Unihack_ Expected Output - Delivery Format.csv"
)

ACTUAL = (
    "data/output/"
    "final_enriched_products.csv"
)


def main():

    expected = pd.read_csv(EXPECTED)
    actual = pd.read_csv(ACTUAL)

    print("=" * 70)
    print("EVALUATION SCHEMA DIAGNOSTIC")
    print("=" * 70)

    print("\nEXPECTED")
    print("Rows:", len(expected))
    print("Columns:", len(expected.columns))

    for column in expected.columns:
        print(" -", repr(column))

    print("\nACTUAL")
    print("Rows:", len(actual))
    print("Columns:", len(actual.columns))

    for column in actual.columns:
        print(" -", repr(column))

    expected_set = {
        str(column).strip()
        for column in expected.columns
    }

    actual_set = {
        str(column).strip()
        for column in actual.columns
    }

    print("\nCOMMON COLUMNS")

    common = sorted(
        expected_set & actual_set
    )

    if common:
        for column in common:
            print(" -", column)
    else:
        print("NONE")

    print("\nEXPECTED-ONLY")

    for column in sorted(
        expected_set - actual_set
    ):
        print(" -", column)

    print("\nACTUAL-ONLY")

    for column in sorted(
        actual_set - expected_set
    ):
        print(" -", column)


if __name__ == "__main__":
    main()