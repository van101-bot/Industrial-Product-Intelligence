from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import pandas as pd


@dataclass
class LOVProfile:
    """
    Internal representation of a company's controlled vocabulary.

    The profile deliberately keeps the source structure visible so
    downstream enrichment can explain where a value came from.
    """

    source_file: str = ""

    taxonomy_paths: list[str] = field(default_factory=list)

    attribute_labels: list[str] = field(default_factory=list)

    attribute_values: dict[str, list[str]] = field(default_factory=dict)

    normalized_labels: dict[str, str] = field(default_factory=dict)

    normalized_values: dict[str, dict[str, str]] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key):
        return self.summary()[key]
    
    def summary(self) -> dict:
        return {
            "source_file": self.source_file,
            "taxonomy_count": len(self.taxonomy_paths),
            "attribute_count": len(self.attribute_labels),
            "controlled_value_count": sum(
                len(values)
                for values in self.attribute_values.values()
            ),
        }


def _clean(value) -> str:
    if pd.isna(value):
        return ""

    return str(value).strip()


def _find_column(df: pd.DataFrame, candidates: list[str]):
    lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]

    return None


def profile_dataframe(
    df: pd.DataFrame,
    source_file: str = "",
) -> LOVProfile:

    profile = LOVProfile(
        source_file=source_file
    )

    columns = list(df.columns)

    classpath_col = _find_column(
        df,
        [
            "Classpath",
            "Class Path",
            "Taxonomy",
            "Category",
            "Category Path",
        ],
    )

    leaf_col = _find_column(
        df,
        [
            "Leaf Node",
            "Leaf",
            "Category Leaf",
        ],
    )

    attribute_col = _find_column(
        df,
        [
            "Attribute Label",
            "Attribute",
            "Attribute Name",
        ],
    )

    value_col = _find_column(
        df,
        [
            "Attribute Values",
            "Attribute Value",
            "Values",
            "Allowed Values",
        ],
    )

    normalized_label_col = _find_column(
        df,
        [
            "Normalized Label",
            "Normalized Attribute",
        ],
    )

    normalized_value_col = _find_column(
        df,
        [
            "Normalized Values",
            "Normalized Value",
        ],
    )

    # ---------------------------------------------------------
    # TAXONOMY
    # ---------------------------------------------------------

    if classpath_col:
        for value in df[classpath_col].dropna():
            value = _clean(value)

            if value:
                profile.taxonomy_paths.append(value)

    if leaf_col:
        for value in df[leaf_col].dropna():
            value = _clean(value)

            if value and value not in profile.taxonomy_paths:
                profile.taxonomy_paths.append(value)

    profile.taxonomy_paths = sorted(
        set(profile.taxonomy_paths)
    )

    # ---------------------------------------------------------
    # ATTRIBUTES + CONTROLLED VALUES
    # ---------------------------------------------------------

    if attribute_col:

        for _, row in df.iterrows():

            attribute = _clean(
                row.get(attribute_col, "")
            )

            if not attribute:
                continue

            if attribute not in profile.attribute_labels:
                profile.attribute_labels.append(attribute)

            if value_col:

                raw_values = _clean(
                    row.get(value_col, "")
                )

                if raw_values:

                    values = [
                        item.strip()
                        for item in raw_values.split(",")
                        if item.strip()
                    ]

                    existing = profile.attribute_values.setdefault(
                        attribute,
                        []
                    )

                    for value in values:
                        if value not in existing:
                            existing.append(value)

            if normalized_label_col:

                normalized_label = _clean(
                    row.get(normalized_label_col, "")
                )

                if normalized_label:
                    profile.normalized_labels[
                        attribute
                    ] = normalized_label

            if normalized_value_col:

                normalized_values = _clean(
                    row.get(normalized_value_col, "")
                )

                if normalized_values:
                    mapping = profile.normalized_values.setdefault(
                        attribute,
                        {}
                    )

                    if value_col:

                        raw_values = _clean(
                            row.get(value_col, "")
                        )

                        if raw_values:
                            raw_list = [
                                item.strip()
                                for item in raw_values.split(",")
                                if item.strip()
                            ]

                            norm_list = [
                                item.strip()
                                for item in normalized_values.split(",")
                                if item.strip()
                            ]

                            for raw, normalized in zip(
                                raw_list,
                                norm_list,
                            ):
                                mapping[raw] = normalized

    profile.attribute_labels = sorted(
        set(profile.attribute_labels)
    )

    return profile


def load_lov_profile(path: str | Path) -> LOVProfile:

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"LOV file not found: {path}"
        )

    if path.suffix.lower() == ".csv":

        df = pd.read_csv(path)

    elif path.suffix.lower() in [".xlsx", ".xls"]:

        df = pd.read_excel(
            path
        )

    else:

        raise ValueError(
            f"Unsupported LOV format: {path.suffix}"
        )

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return profile_dataframe(
        df,
        source_file=str(path),
    )