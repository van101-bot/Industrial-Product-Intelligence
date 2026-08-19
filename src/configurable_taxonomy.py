from pathlib import Path
import pandas as pd
import re


class ConfigurableTaxonomy:

    def __init__(self, path: str):

        self.path = Path(path)

        self.df = pd.read_csv(self.path)

        required = {
            "taxonomy",
            "aliases",
        }

        missing = required - set(self.df.columns)

        if missing:
            raise ValueError(
                f"Taxonomy LOV missing: {missing}"
            )

    def classify(self, description: str):

        text = str(description or "").lower()

        best = None

        for _, row in self.df.iterrows():

            taxonomy = str(
                row["taxonomy"]
            ).strip()

            aliases = str(
                row["aliases"]
            ).split(";")

            for alias in aliases:

                alias = alias.strip().lower()

                if not alias:
                    continue

                if re.search(
                    r"\b" +
                    re.escape(alias) +
                    r"\b",
                    text,
                ):

                    score = 1.0

                    candidate = {
                        "category": taxonomy,
                        "confidence": score,
                        "source": "company_lov",
                        "evidence": alias,
                    }

                    if (
                        best is None
                        or score > best["confidence"]
                    ):
                        best = candidate

        if best:
            return best

        return {
            "category": None,
            "confidence": 0.0,
            "source": "lov_unresolved",
            "evidence": None,
        }