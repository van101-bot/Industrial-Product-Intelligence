from pathlib import Path
import json
import pandas as pd


def _safe_rate(numerator, denominator):
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def build_quality_report(df: pd.DataFrame) -> dict:

    total = len(df)

    report = {
        "total_rows": total,
        "columns": len(df.columns),
    }

    if "mpn" in df.columns:
        report["mpn_present_rate"] = _safe_rate(
            df["mpn"].notna().sum(),
            total
        )

    if "brand" in df.columns:
        report["brand_present_rate"] = _safe_rate(
            df["brand"].notna().sum(),
            total
        )

    if "manufacturer" in df.columns:
        report["manufacturer_present_rate"] = _safe_rate(
            df["manufacturer"].notna().sum(),
            total
        )

    if "product_type" in df.columns:
        report["product_type_present_rate"] = _safe_rate(
            df["product_type"].notna().sum(),
            total
        )

    if "taxonomy" in df.columns:
        report["taxonomy_resolved_rate"] = _safe_rate(
            df["taxonomy"].notna().sum(),
            total
        )

    if "evidence_count" in df.columns:
        report["rows_with_evidence"] = int(
            (df["evidence_count"] > 0).sum()
        )

    if "status" in df.columns:
        report["status_distribution"] = (
            df["status"]
            .fillna("unknown")
            .value_counts()
            .to_dict()
        )

    return report


def save_quality_report(
    df: pd.DataFrame,
    output_path: str
):

    report = build_quality_report(df)

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2,
            default=str
        )

    return report