import re
import pandas as pd


def normalize_identifier(value):

    if pd.isna(value):
        return ""

    value = str(value).upper().strip()

    return re.sub(
        r"[^A-Z0-9]",
        "",
        value
    )


def detect_duplicate_ids(
    df: pd.DataFrame,
    id_column: str = "mpn",
):

    result = df.copy()

    result["_normalized_id"] = (
        result[id_column]
        .apply(normalize_identifier)
    )

    duplicates = (
        result["_normalized_id"]
        .duplicated(keep=False)
    )

    result["duplicate_flag"] = duplicates

    return result