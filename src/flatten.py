import pandas as pd
from .utils import parse_dict, build_search_text

def flatten_enriched_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten enriched product dataframe into final enriched format.
    Ensures PART_NUMBER, Mfg_Part_Num, Part_Desc are populated.
    """
    records = []

    for _, row in df.iterrows():
        parsed = parse_dict(row.get("attributes", {}))

        part_number = row.get("PART_NUMBER", "").strip()
        mfg_part_num = row.get("Mfg_Part_Num", "").strip()
        description = row.get("Part_Desc", "").strip()
        brand = row.get("E1_Brand", "").strip()
        manuf = row.get("Part_Manuf", "").strip()

        # Build search text from multiple fields
        search_text = build_search_text(
            part_number, mfg_part_num, description, brand, manuf
        )

        records.append({
            "PART_NUMBER": part_number or parsed.get("part_number", ""),
            "Mfg_Part_Num": mfg_part_num or parsed.get("mpn", ""),
            "Part_Desc": description or parsed.get("description", ""),
            "E1_Brand": brand or parsed.get("brand", ""),
            "Part_Manuf": manuf or parsed.get("manufacturer", ""),
            "Search_Text": search_text,
        })

    return pd.DataFrame(records)
