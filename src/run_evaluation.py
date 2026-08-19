from pathlib import Path

import pandas as pd

from src.evaluation_engine import (
    evaluate,
    print_report,
)


EXPECTED_FILE = (
    "Unihack_ Expected Output - Delivery Format.csv"
)

ACTUAL_FILE = (
    "data/output/final_enriched_products.csv"
)


def find_file(filename):

    matches = list(
        Path(".").rglob(filename)
    )

    if not matches:
        raise FileNotFoundError(
            f"Could not find {filename}"
        )

    return matches[0]


def main():

    expected_path = find_file(
        EXPECTED_FILE
    )

    actual_path = find_file(
        Path(ACTUAL_FILE).name
    )

    print(
        "EXPECTED:",
        expected_path,
    )

    print(
        "ACTUAL:",
        actual_path,
    )

    expected = pd.read_csv(
        expected_path
    )

    actual = pd.read_csv(
        actual_path
    )

    # Only evaluate fields that are
    # actually present in BOTH datasets.
    preferred_fields = [
        "Mfg_Part_Num",
        "Part_Desc",
        "brand",
        "manufacturer",
        "product_type",
        "taxonomy",
        "diameter",
        "thickness",
        "arbor",
        "length",
        "width",
        "height",
        "pack_quantity",
    ]

    fields = [
        field
        for field in preferred_fields
        if (
            field in expected.columns
            and field in actual.columns
        )
    ]

    print(
        "\nEVALUATING:",
        fields,
    )

    result = evaluate(
        expected,
        actual,
        fields,
    )

    print_report(
        result
    )


if __name__ == "__main__":
    main()