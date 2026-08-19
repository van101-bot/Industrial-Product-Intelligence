import pandas as pd

from src.final_output import flatten_enriched_dataframe

import ast

def parse_dict(value: str) -> dict:
    """
    Safely parse a stringified dictionary into a Python dict.
    Handles cases where the value is already a dict.
    """
    if isinstance(value, dict):
        return value
    if not value:
        return {}
    try:
        return ast.literal_eval(value)
    except Exception:
        return {}

def build_search_text(values: list[str]) -> str:
    """
    Build a search-ready text string from a list of values.
    Filters out None/empty values and joins them with spaces.
    """
    return " ".join(str(v) for v in values if v)

def test_final_output_is_flat():

    df = pd.DataFrame([
        {
            "Mfg_Part_Num": "49-94-0107",
            "Part_Desc": (
                '49-94-0107 Milw 4-1/2"x.045"x7/8" '
                "Performance+ Metal Cut Off Disc"
            ),
            "status": "accepted",
            "identity": str({
                "mpn": "49-94-0107",
                "description": "Performance+ Metal Cut Off Disc",
            }),
            "brand": str({
                "brand": "Milwaukee",
            }),
            "manufacturer": str({
                "value": "Milwaukee Accessory",
            }),
            "attributes": str({
                "normalized": {
                    "diameter": 4.5,
                    "thickness": 0.045,
                    "arbor": 0.875,
                    "product_type": "Metal Cut Off Disc",
                    "pack_quantity": None,
                },
                "confidence": {
                    "diameter": 0.85,
                    "thickness": 0.85,
                    "arbor": 0.85,
                },
            }),
            "evidence_count": 3,
        }
    ])

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
    
               "search_text": build_search_text(
                    identity.get("mpn")
                        or row.get("Mfg_Part_Num"),
    
                    brand.get("brand"),
    
                    manufacturer.get("value")
                        or identity.get("manufacturer_candidate"),
    
                    normalized.get("product_type"),
    
                    normalized.get("diameter"),
    
                    normalized.get("thickness"),
    
                    normalized.get("arbor"),
    
                    normalized.get("pack_quantity"),
                ),
            }
        result = flatten_enriched_dataframe(df)

        assert len(result) == 1

        assert result.iloc[0]["mpn"] == "49-94-0107"

        assert result.iloc[0]["diameter"] == 4.5
        assert result.iloc[0]["thickness"] == 0.045
        assert result.iloc[0]["arbor"] == 0.875

        assert result.iloc[0]["product_type"] == (
        "Metal Cut Off Disc"
    )

        assert "49-94-0107" in result.iloc[0]["search_text"]
        assert "Metal Cut Off Disc" in result.iloc[0]["search_text"]

def test_final_output_contains_core_enrichment_fields():
    import pandas as pd

    actual = pd.read_csv(
        "data/output/final_enriched_products.csv"
    )

    required = {
        "mpn",
        "description",
        "brand",
        "manufacturer",
        "product_type",
        "status",
        "evidence_count",
        "confidence",
        "search_text",
    }

    missing = required - set(actual.columns)

    assert not missing, (
        f"Missing core enrichment columns: {missing}"
    )