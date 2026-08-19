from __future__ import annotations

import pandas as pd


def check_identifier_overlap(
    expected: pd.DataFrame,
    actual: pd.DataFrame,
    id_column: str = "PART_NUMBER",
) -> dict:

    if id_column not in expected.columns:
        raise ValueError(
            f"Expected dataset missing {id_column}"
        )

    if id_column not in actual.columns:
        raise ValueError(
            f"Actual dataset missing {id_column}"
        )

    expected_ids = set(
        expected[id_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    actual_ids = set(
        actual[id_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    overlap = expected_ids & actual_ids

    return {
        "expected_ids": len(expected_ids),
        "actual_ids": len(actual_ids),
        "overlap": len(overlap),
        "overlap_ids": sorted(overlap),
        "evaluatable": len(overlap) > 0,
    }