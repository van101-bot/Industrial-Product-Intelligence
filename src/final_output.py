import ast
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXPECTED_SCHEMA_FILE = BASE_DIR / "data" / "raw" / "Unihack_ Expected Output - Delivery Format.csv"

def build_final_output(enriched: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten enriched dataframe and align it to the expected 252-column delivery format.
    Missing columns will be filled with blanks.
    Map enriched product fields into the 252-column delivery format.
    Missing columns are filled with blanks.
    """

    # Load expected schema
    expected = pd.read_csv(EXPECTED_SCHEMA_FILE, nrows=0)
    schema_cols = expected.columns

    # Create a blank delivery dataframe
    final = pd.DataFrame("", index=enriched.index, columns=schema_cols)

    # Map enriched fields into delivery schema
    if "PART_NUMBER" in enriched.columns:
        final["PART_NUMBER"] = enriched["PART_NUMBER"]

    if "Mfg_Part_Num" in enriched.columns:
        final["Mfg_Part_Num"] = enriched["Mfg_Part_Num"]
        # use Mfg_Part_Num as PART_NUMBER if PART_NUMBER is missing
        final["PART_NUMBER"] = enriched.get("PART_NUMBER", enriched["Mfg_Part_Num"])
    
    if "Part_Desc" in enriched.columns:
        final["Part_Desc"] = enriched["Part_Desc"]

    if "E1_Brand" in enriched.columns:
        final["E1_Brand"] = enriched["E1_Brand"]

    if "Part_Manuf" in enriched.columns:
        final["Part_Manuf"] = enriched["Part_Manuf"]

    final["MANUFACTURER_NAME"] = enriched.get("MANUFACTURER_NAME", "")
    final["BRAND_NAME"] = enriched.get("BRAND_NAME", "")

    # Manufacturer URLs
    if "MFR_URL" in enriched.columns:
        final["MFR URL"] = enriched["MFR_URL"]

    for i in range(1, 6):
        col = f"Ref_URL_{i}"
        if col in enriched.columns:
            final[f"Ref URL {i}"] = enriched[col]

    # Add other mappings as needed for your schema


    # Add more mappings here as needed for other enriched fields

    return final

    

def parse_dict(value):
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
    for column in ["mpn","brand","manufacturer","product_type","diameter","thickness","arbor","length","width","height"]:
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
    records = []
    for _, row in df.iterrows():
        identity = parse_dict(row.get("identity"))
        brand = parse_dict(row.get("brand"))
        manufacturer = parse_dict(row.get("manufacturer"))
        attributes = parse_dict(row.get("attributes"))

        normalized = attributes.get("normalized", {})
        confidence = attributes.get("confidence", {})

        record = {
            "mpn": identity.get("mpn") or row.get("Mfg_Part_Num"),
            "description": identity.get("description") or row.get("Part_Desc"),
            "brand": brand.get("brand"),
            "manufacturer": manufacturer.get("value") or identity.get("manufacturer_candidate"),
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
            "search_text": build_search_text(row),
        }
        records.append(record)
    return pd.DataFrame(records)

def determine_status(row):
    evidence_count = int(row.get("evidence_count", 0) or 0)
    confidence = row.get("confidence", {})
    if isinstance(confidence, dict):
        values = [float(v) for v in confidence.values() if isinstance(v, (int, float))]
        min_confidence = min(values) if values else 0.0
    else:
        min_confidence = float(confidence or 0.0)
    if evidence_count == 0:
        return "needs_review"
    if min_confidence < 0.5:
        return "needs_review"
    return "accepted"
