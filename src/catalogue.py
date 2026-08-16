import pandas as pd

from .pipeline import enrich_product


def enrich_catalogue(input_path: str) -> pd.DataFrame:
    """
    Enrich every product in the input catalogue.

    Returns a DataFrame containing the original product information
    plus enrichment status, identity, attributes, and evidence.
    """

    df = pd.read_csv(input_path)

    results = []

    for _, row in df.iterrows():

        try:
            result = enrich_product(row)

            results.append({
                "Mfg_Part_Num": row.get("Mfg_Part_Num"),
                "Part_Desc": row.get("Part_Desc"),
                "status": result.get("status", "unknown"),
                "identity": result.get("identity"),
                "brand": result.get("brand"),
                "manufacturer": result.get("manufacturer"),
                "attributes": result.get("attributes"),
                "evidence": result.get("evidence", []),
            })

        except Exception as exc:

            results.append({
                "Mfg_Part_Num": row.get("Mfg_Part_Num"),
                "Part_Desc": row.get("Part_Desc"),
                "status": "error",
                "error": str(exc),
            })

    return pd.DataFrame(results)