from pathlib import Path
import pandas as pd


class CompanyLOV:

    def __init__(self, path: str):

        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(
                f"LOV file not found: {self.path}"
            )

        self.df = pd.read_csv(self.path)

        required = {
            "attribute",
            "controlled_value",
            "aliases",
        }

        missing = required - set(self.df.columns)

        if missing:
            raise ValueError(
                f"LOV missing columns: {missing}"
            )

    def attributes(self):

        return sorted(
            self.df["attribute"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

    def values(self, attribute):

        rows = self.df[
            self.df["attribute"]
            .astype(str)
            .str.strip()
            == attribute
        ]

        return (
            rows["controlled_value"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

    def resolve(
        self,
        attribute: str,
        value: str,
    ):

        value = str(value).strip().lower()

        rows = self.df[
            self.df["attribute"]
            .astype(str)
            .str.strip()
            == attribute
        ]

        for _, row in rows.iterrows():

            canonical = str(
                row["controlled_value"]
            ).strip()

            aliases = str(
                row["aliases"]
            ).split(";")

            candidates = [
                canonical.lower()
            ]

            candidates.extend(
                alias.strip().lower()
                for alias in aliases
            )

            if value in candidates:

                return {
                    "value": canonical,
                    "confidence": 1.0,
                    "source": "company_lov",
                }

        return {
            "value": None,
            "confidence": 0.0,
            "source": "lov_unresolved",
        }