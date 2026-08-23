import pandas as pd

from .pipeline import enrich_product


def enrich_catalogue(input_path: str, company_lov=None) -> pd.DataFrame:
    """
    Enrich a catalogue row-by-row.

    Each product is isolated so one failure cannot stop
    the entire catalogue.
    """

    df = pd.read_csv(input_path)

    results = []

    total = len(df)

    for index, (_, row) in enumerate(df.iterrows(), start=1):

        print(
            f"\rProcessing {index}/{total}",
            end="",
            flush=True,
        )

        try:
            result = enrich_product(row)

            attributes = result.get("attributes") or {}

            evidence = (
                attributes.get("evidence", [])
                if isinstance(attributes, dict)
                else []
            )

            results.append({
                "Mfg_Part_Num": row.get("Mfg_Part_Num"),
                "Part_Desc": row.get("Part_Desc"),

                "status": (
                    attributes.get("status", "unknown")
                    if isinstance(attributes, dict)
                    else "unknown"
                ),

                "identity": result.get("identity"),
                "brand": result.get("brand"),
                "manufacturer": result.get("manufacturer"),

                "attributes": attributes,

                "evidence_count": len(evidence),
            })

        
except Exception as exc:

    print(
        f"\nERROR at row {index}: "
        f"{type(exc).__name__}: {exc}"
    )

    results.append({
        "Mfg_Part_Num": row.get("Mfg_Part_Num"),
        "Part_Desc": row.get("Part_Desc"),
        "status": "error",
        "identity": None,
        "brand": None,
        "manufacturer": None,
        "attributes": None,
        "evidence_count": 0,
        "error": f"{type(exc).__name__}: {exc}",
    })
