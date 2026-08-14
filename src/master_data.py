from functools import lru_cache
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


def _find_file(filename: str) -> Path:
    candidates = [
        BASE_DIR / "data" / "raw" / filename,
        BASE_DIR / "data" / filename,
        BASE_DIR / filename,
    ]

    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"Could not find {filename}. Checked: {candidates}"
    )


@lru_cache(maxsize=1)
def load_manufacturer_brand_master() -> pd.DataFrame:
    """
    Build a lightweight manufacturer/brand reference master
    from the challenge input dataset.

    The challenge does not provide a separate master-data file,
    so we derive the reference values from the available columns.
    """

    filename = "Unihack_ Sample Dataset - Input.csv"
    path = _find_file(filename)

    df = pd.read_csv(path)

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    required = {
        "Part_Manuf",
        "E1_Brand",
        "DIB_Brand",
        "Unilog_Brand",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Input dataset missing required columns: {missing}"
        )

    manufacturers = (
        df["Part_Manuf"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    manufacturers = manufacturers[
        (manufacturers != "") &
        (manufacturers != "-")
    ]

    manufacturer_rows = []

    for value in manufacturers.unique():
        if "(" in value and value.endswith(")"):
            name, code = value.rsplit("(", 1)
            name = name.strip()
            code = code[:-1].strip()
        else:
            name = value
            code = ""

        manufacturer_rows.append({
            "MANUFACTURER_NAME": name,
            "MANUFACTURER_CODE": code,
        })

    manufacturer_df = pd.DataFrame(manufacturer_rows)

    brand_series = pd.concat(
        [
            df["E1_Brand"],
            df["Unilog_Brand"],
            df["DIB_Brand"],
        ],
        ignore_index=True,
    )

    brands = (
        brand_series
        .dropna()
        .astype(str)
        .str.strip()
    )

    placeholder_prefixes = (
        "--",
        "COMMODITY - UNBRANDED",
    )

    brands = brands[
        ~brands.str.startswith(placeholder_prefixes)
    ]

    brands = brands[
        brands != ""
    ]

    brand_rows = []

    for value in brands.unique():
        brand_rows.append({
            "BRAND_NAME": value,
            "BRAND_CODE": "",
        })

    brand_df = pd.DataFrame(brand_rows)

    # Create a master-like structure expected by the rest
    # of the enrichment pipeline.
    result = pd.DataFrame(
        columns=[
            "MANUFACTURER_NAME",
            "MANUFACTURER_CODE",
            "BRAND_NAME",
            "BRAND_CODE",
        ]
    )

    manufacturer_count = len(manufacturer_df)
    brand_count = len(brand_df)
    total = max(manufacturer_count, brand_count)

    result = pd.DataFrame({
        "MANUFACTURER_NAME": (
            list(manufacturer_df["MANUFACTURER_NAME"])
            + [""] * (total - manufacturer_count)
        ),
        "MANUFACTURER_CODE": (
            list(manufacturer_df["MANUFACTURER_CODE"])
            + [""] * (total - manufacturer_count)
        ),
        "BRAND_NAME": (
            list(brand_df["BRAND_NAME"])
            + [""] * (total - brand_count)
        ),
        "BRAND_CODE": (
            list(brand_df["BRAND_CODE"])
            + [""] * (total - brand_count)
        ),
    })

    return result


def manufacturer_names() -> list[str]:
    df = load_manufacturer_brand_master()

    return [
        value
        for value in df["MANUFACTURER_NAME"].dropna().unique()
        if str(value).strip()
    ]


def brand_names() -> list[str]:
    df = load_manufacturer_brand_master()

    return [
        value
        for value in df["BRAND_NAME"].dropna().unique()
        if str(value).strip()
    ]