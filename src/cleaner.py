from typing import Optional

import pandas as pd


PLACEHOLDERS = {
    "-- Unbranded --",
    "-- No Unilog Brand --",
    "-- No DIB Brand --",
    "",
    "N/A",
    "NA",
    "NULL",
    "None",
}


def clean_value(value) -> Optional[str]:
    """
    Normalize a raw catalog value.

    Placeholder values are converted to None.
    Real values are stripped of unnecessary whitespace.
    """
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in PLACEHOLDERS:
        return None

    return value


def clean_product_row(row: pd.Series) -> dict:
    """
    Convert one raw catalog row into a clean product record.
    """

    return {
        "mpn": clean_value(row["Mfg_Part_Num"]),
        "part_description": clean_value(row["Part_Desc"]),
        "e1_brand": clean_value(row["E1_Brand"]),
        "unilog_brand": clean_value(row["Unilog_Brand"]),
        "dib_brand": clean_value(row["DIB_Brand"]),
        "manufacturer": clean_value(row["Part_Manuf"]),
    }