import ast
import pandas as pd


def parse_dict(value):
    """
    Convert a CSV string representation of a dictionary
    back into a Python dictionary.
    """
    if isinstance(value, dict):
        return value

    if pd.isna(value):
        return {}

    try:
        parsed = ast.literal_eval(str(value))
        return parsed if isinstance(parsed, dict) else {}
    except (ValueError, SyntaxError):
        return {}


def build_search_text(row):
    parts = []

    for column in [
        "mpn",
        "brand",
        "manufacturer",
        "product_type",
        "diameter",
        "thickness",
        "arbor",
        "length",
        "width",
        "height",
    ]:
        value = row.get(column)

        if value is None or pd.isna(value):
            continue

        value = str(value).strip()

        if value:
            parts.append(value)

    pack = row.get("pack_quantity")

    if pack is not None and not pd.isna(pack):
        try:
            pack = int(float(pack))
            parts.append(f"{pack} pcs")
        except (ValueError, TypeError):
            pass

    return " | ".join(parts)

def flatten_enriched_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert nested enrichment output into a flat,
    search-ready dataframe.
    """

    records = []

    for _, row in df.iterrows():

        identity = parse_dict(row.get("identity"))
        brand = parse_dict(row.get("brand"))
        manufacturer = parse_dict(row.get("manufacturer"))
        attributes = parse_dict(row.get("attributes"))

        normalized = attributes.get("normalized", {})
        confidence = attributes.get("confidence", {})

        record = {
            "mpn": identity.get("mpn")
                            or row.get("Mfg_Part_Num"),
            
                        "description": identity.get("description")
                            or row.get("Part_Desc"),
            
                        "brand": brand.get("brand"),
            
                        "manufacturer": manufacturer.get("value")
                            or identity.get("manufacturer_candidate"),
            
                        "product_type": normalized.get("product_type"),
            
                        "diameter": normalized.get("diameter"),
            
                        "thickness": normalized.get("thickness"),
            
                        "arbor": normalized.get("arbor"),
            
                        "length": normalized.get("length"),
            
                        "width": normalized.get("width"),
            
                        "height": normalized.get("height"),
            
                        "pack_quantity": normalized.get("pack_quantity"),
            
                        "status": row.get("status"),
            
                        "evidence_count": row.get("evidence_count", 0),
            
                        "confidence": confidence,
            
                        "search_text": build_search_text([
                            identity.get("mpn") or row.get("Mfg_Part_Num"),
                            brand.get("brand"),
                            manufacturer.get("value") or identity.get("manufacturer_candidate"),
                            normalized.get("product_type"),
                            normalized.get("diameter"),
                            normalized.get("thickness"),
                            normalized.get("arbor"),
                            normalized.get("pack_quantity"),
                            normalized.get("length"),
                            normalized.get("width"),
                            normalized.get("height"),
                            ]),
                                                   
        }

        records.append(record)

    return pd.DataFrame(records)

def determine_status(row):
    evidence_count = int(row.get("evidence_count", 0) or 0)
    confidence = row.get("confidence", {})

    if isinstance(confidence, dict):
        values = [
            float(v)
            for v in confidence.values()
            if isinstance(v, (int, float))
        ]
        min_confidence = min(values) if values else 0.0
    else:
        min_confidence = float(confidence or 0.0)

    if evidence_count == 0:
        return "needs_review"

    if min_confidence < 0.5:
        return "needs_review"

    return "accepted"