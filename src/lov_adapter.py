from pathlib import Path
import pandas as pd


PLACEHOLDER_VALUES = {
    "",
    "-",
    "--",
    "-- Unbranded --",
    "-- No Unilog Brand --",
    "-- No DIB Brand --",
    "COMMODITY - UNBRANDED",
}


class LOVAdapter:
    """
    Generic adapter for a customer-provided LOV workbook.

    The adapter intentionally does not assume one exact workbook
    layout. It discovers likely taxonomy/value columns and exposes
    normalized vocabularies to the enrichment pipeline.
    """

    def __init__(self, source=None):
        self.source = source
        self.tables = {}

        if source is not None:
            self._load(source)

    def _load(self, source):
        path = Path(source)

        if path.suffix.lower() in {".xlsx", ".xls"}:
            workbook = pd.ExcelFile(path)

            for sheet in workbook.sheet_names:
                df = pd.read_excel(path, sheet_name=sheet)

                df.columns = [
                    str(column).strip()
                    for column in df.columns
                ]

                self.tables[sheet] = df

        elif path.suffix.lower() == ".csv":
            df = pd.read_csv(path)

            df.columns = [
                str(column).strip()
                for column in df.columns
            ]

            self.tables[path.stem] = df

        else:
            raise ValueError(
                f"Unsupported LOV format: {path.suffix}"
            )

    @property
    def sheet_names(self):
        return list(self.tables.keys())

    def _clean_values(self, values):
        cleaned = []

        for value in values:
            if pd.isna(value):
                continue

            value = str(value).strip()

            if value in PLACEHOLDER_VALUES:
                continue

            if value:
                cleaned.append(value)

        return sorted(set(cleaned))

    def find_columns(self, keywords):
        """
        Find columns whose names contain any supplied keyword.
        """
        matches = []

        for sheet, df in self.tables.items():
            for column in df.columns:
                normalized = str(column).lower()

                if any(
                    keyword.lower() in normalized
                    for keyword in keywords
                ):
                    matches.append(
                        (sheet, column)
                    )

        return matches

    def taxonomy_values(self):
        """
        Discover likely taxonomy/category/classpath columns.
        """
        candidates = self.find_columns(
            [
                "classpath",
                "taxonomy",
                "category",
                "leaf node",
                "class",
            ]
        )

        values = []

        for sheet, column in candidates:
            values.extend(
                self.tables[sheet][column]
                .tolist()
            )

        return self._clean_values(values)

    def attribute_values(self):
        """
        Discover likely attribute-label/value columns.
        """
        candidates = self.find_columns(
            [
                "attribute",
                "normalized label",
                "attribute label",
            ]
        )

        values = []

        for sheet, column in candidates:
            values.extend(
                self.tables[sheet][column]
                .tolist()
            )

        return self._clean_values(values)

    def summary(self):
        return {
            "sheets": self.sheet_names,
            "taxonomy_values": len(
                self.taxonomy_values()
            ),
            "attribute_values": len(
                self.attribute_values()
            ),
        }