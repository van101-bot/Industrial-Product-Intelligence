from pathlib import Path
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

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "output"
    / "final_delivery_format.csv"
)


def load_expected_schema() -> list[str]:
    """
    Load the official competition delivery headers.

    Headers are preserved exactly and in exactly the same order.
    """

    expected = pd.read_csv(
        EXPECTED_FILE,
        nrows=0
    )

    return list(expected.columns)


def load_actual() -> pd.DataFrame:
    return pd.read_csv(ACTUAL_FILE)


def clean_value(value):
    """
    Convert empty/NaN values to blank strings for delivery.
    Never invent values.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


def first_nonempty(*values):
    """
    Return the first usable value.
    """

    for value in values:
        if value is not None and not pd.isna(value):
            value = str(value).strip()

            if value:
                return value

    return ""


def build_delivery_output(
    actual: pd.DataFrame,
    expected_columns: list[str],
) -> pd.DataFrame:

    output = pd.DataFrame(
        "",
        index=range(len(actual)),
        columns=expected_columns,
    )

    # ------------------------------------------------------------
    # INPUT IDENTITY FIELDS
    # ------------------------------------------------------------

    if "mpn" in actual.columns:

        if "Mfg_Part_Num" in output.columns:
            output["Mfg_Part_Num"] = actual["mpn"].map(clean_value)

        if "MANUFACTURER_PART_NUMBER" in output.columns:
            output["MANUFACTURER_PART_NUMBER"] = (
                actual["mpn"].map(clean_value)
            )

        if "PART_NUMBER" in output.columns:
            output["PART_NUMBER"] = actual["mpn"].map(clean_value)

    # ------------------------------------------------------------
    # ORIGINAL DESCRIPTION
    # ------------------------------------------------------------

    if "description" in actual.columns:

        if "Part_Desc" in output.columns:
            output["Part_Desc"] = actual["description"].map(
                clean_value
            )

    # ------------------------------------------------------------
    # BRAND
    # ------------------------------------------------------------

    if "brand" in actual.columns:

        if "BRAND_NAME" in output.columns:
            output["BRAND_NAME"] = actual["brand"].map(
                clean_value
            )

        if "E1_Brand" in output.columns:
            output["E1_Brand"] = actual["brand"].map(
                clean_value
            )

    # ------------------------------------------------------------
    # MANUFACTURER
    # ------------------------------------------------------------

    if "manufacturer" in actual.columns:

        if "MANUFACTURER_NAME" in output.columns:
            output["MANUFACTURER_NAME"] = (
                actual["manufacturer"].map(clean_value)
            )

        if "Part_Manuf" in output.columns:
            output["Part_Manuf"] = (
                actual["manufacturer"].map(clean_value)
            )

    # ------------------------------------------------------------
    # PRODUCT TYPE / CLASSIFICATION
    # ------------------------------------------------------------

    if "product_type" in actual.columns:

        if "Product Name" in output.columns:
            output["Product Name"] = actual["product_type"].map(
                clean_value
            )

    # ------------------------------------------------------------
    # DIMENSIONS
    # ------------------------------------------------------------

    dimension_mapping = {
        "length": "LENGTH",
        "width": "WIDTH",
        "height": "HEIGHT",
    }

    for source, target in dimension_mapping.items():

        if source in actual.columns and target in output.columns:
            output[target] = actual[source].map(clean_value)

    # ------------------------------------------------------------
    # PACK QUANTITY
    # ------------------------------------------------------------

    if "pack_quantity" in actual.columns:

        if "Selling Qty" in output.columns:
            output["Selling Qty"] = actual["pack_quantity"].map(
                clean_value
            )

    # ------------------------------------------------------------
    # INTERNAL SEARCH TEXT
    # ------------------------------------------------------------
    #
    # search_text is useful internally but there is no direct
    # official 252-column equivalent, so we deliberately do not
    # place it into an unrelated field.
    #

    return output


def main():

    print("=" * 70)
    print("COMPETITION DELIVERY ADAPTER")
    print("=" * 70)

    print()
    print("EXPECTED SCHEMA:")
    print(EXPECTED_FILE)

    expected_columns = load_expected_schema()

    print("EXPECTED COLUMNS:", len(expected_columns))

    actual = load_actual()

    print("ACTUAL INTERNAL ROWS:", len(actual))
    print("ACTUAL INTERNAL COLUMNS:", len(actual.columns))

    output = build_delivery_output(
        actual,
        expected_columns,
    )

    output.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print()
    print("DELIVERY OUTPUT:")
    print(OUTPUT_FILE)

    print()
    print("ROWS:", len(output))
    print("COLUMNS:", len(output.columns))

    print()
    print("FIRST 15 COLUMNS:")
    for column in output.columns[:15]:
        print(" -", column)

    print()
    print("LAST 10 COLUMNS:")
    for column in output.columns[-10:]:
        print(" -", column)

    print()
    print("SCHEMA CHECK:")

    if list(output.columns) == expected_columns:
        print("PASS — exact 252-column schema")
    else:
        print("FAIL — schema mismatch")


if __name__ == "__main__":
    main()