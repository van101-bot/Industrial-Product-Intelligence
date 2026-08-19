from pathlib import Path
import profile
import profile
from typing import Any
from unittest import result
import pandas as pd

from src.lov_profile import load_lov_profile

class Profile:

    def __init__(
        self,
        name,
        strict_mode=True,
        minimum_confidence=0.90,
    ):

        self.name = name
        self.strict_mode = strict_mode
        self.minimum_confidence = minimum_confidence

    def accept_prediction(self, result: dict) -> bool:
        """
        Decide whether to accept a prediction result
        based on confidence and strict_mode settings.
        """
        if result.get("value") is None:
            return False

        if self.strict_mode:
            return result.get("confidence", 0) >= self.minimum_confidence

        return True
  
PLACEHOLDER_VALUES = {
    "",
    "-",
    "--",
    "-- UNBRANDED --",
    "-- NO UNILOG BRAND --",
    "-- NO DIB BRAND --",
    "N/A",
    "NA",
    "NONE",
    "NULL",
}


def clean_value(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    if text.upper() in PLACEHOLDER_VALUES:
        return None

    return text


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result.columns = [
        str(column).strip()
        for column in result.columns
    ]

    for column in result.columns:
        result[column] = result[column].apply(clean_value)

    return result


def load_table(path: str | Path) -> pd.DataFrame:
    """
    Load CSV or Excel data into a normalized dataframe.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    suffix = path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(path)

    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)

    else:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    return clean_dataframe(df)


def inspect_workbook(path: str | Path) -> dict:
    """
    Inspect an Excel workbook sheet-by-sheet.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"LOV workbook not found: {path}"
        )

    workbook = pd.ExcelFile(path)

    sheets = {}

    for sheet_name in workbook.sheet_names:

        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
        )

        df = clean_dataframe(df)

        sheets[sheet_name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "data": df,
        }

    return {
        "file": str(path),
        "sheet_names": workbook.sheet_names,
        "sheets": sheets,
    }


def detect_taxonomy_columns(columns: list[str]) -> list[str]:
    keywords = (
        "taxonomy",
        "category",
        "classpath",
        "class",
        "department",
        "dept",
        "leaf",
        "subcategory",
    )

    return [
        column
        for column in columns
        if any(
            keyword in column.lower()
            for keyword in keywords
        )
    ]


def detect_attribute_columns(columns: list[str]) -> list[str]:
    keywords = (
        "attribute",
        "attr",
        "property",
        "specification",
        "spec",
        "value",
    )

    return [
        column
        for column in columns
        if any(
            keyword in column.lower()
            for keyword in keywords
        )
    ]


def build_profile(path: str | Path) -> dict:
    """
    Build a normalized profile from an Excel or CSV source.
    """

    path = Path(path)

    if path.suffix.lower() == ".csv":

        df = load_table(path)

        columns = list(df.columns)

        return {
            "file": str(path),
            "format": "csv",
            "sheets": {
                "default": {
                    "rows": len(df),
                    "columns": columns,
                    "taxonomy_columns":
                        detect_taxonomy_columns(columns),
                    "attribute_columns":
                        detect_attribute_columns(columns),
                }
            },
        }

    inspection = inspect_workbook(path)

    profile = {
        "file": inspection["file"],
        "format": "excel",
        "sheets": {},
    }

    for sheet_name, sheet in inspection["sheets"].items():

        columns = sheet["columns"]

        profile["sheets"][sheet_name] = {
            "rows": sheet["rows"],
            "columns": columns,
            "taxonomy_columns":
                detect_taxonomy_columns(columns),
            "attribute_columns":
                detect_attribute_columns(columns),
        }

    return profile
def load_profile(path):
    """
    Public profile-loading entry point.

    Keeps the configurable LOV API explicit while
    preserving the existing lov_profile implementation.
    """
    return load_lov_profile(path)