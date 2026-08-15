from pathlib import Path
import pandas as pd


INPUT_FILE = "Unihack_ Sample Dataset - Input.csv"


def _find_input_file() -> Path:

    # Search anywhere under data/
    matches = list(
        Path("data").rglob(INPUT_FILE)
    )

    if matches:
        return matches[0]

    raise FileNotFoundError(
        f"Could not find '{INPUT_FILE}' under data/"
    )


def load_lov() -> pd.DataFrame:
    """
    Temporary taxonomy source.

    The competition resources available to us do not
    include the LOV workbook, so we derive a lightweight
    taxonomy vocabulary from the actual catalogue data.

    We will NOT invent controlled LOV values.
    """

    path = _find_input_file()

    df = pd.read_csv(path)

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


def get_product_descriptions() -> list[str]:

    df = load_lov()

    return (
        df["Part_Desc"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )


def get_manufacturers() -> list[str]:

    df = load_lov()

    return (
        df["Part_Manuf"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )


def get_brands() -> list[str]:

    df = load_lov()

    values = []

    for column in [
        "E1_Brand",
        "Unilog_Brand",
        "DIB_Brand",
    ]:

        if column in df.columns:

            values.extend(
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

    return sorted(set(values))