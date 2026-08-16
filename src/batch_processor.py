import pandas as pd

from .pipeline import enrich_product


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    results = []

    for index, row in df.iterrows():

        try:

            result = enrich_product(row)

            results.append({
                "Mfg_Part_Num": row.get("Mfg_Part_Num"),
                "Part_Desc": row.get("Part_Desc"),

                "Brand": result.get("brand"),
                "Manufacturer": result.get("manufacturer"),

                "Product_Type": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("product_type")
                ),

                "Diameter": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("diameter")
                ),

                "Thickness": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("thickness")
                ),

                "Arbor": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("arbor")
                ),

                "Length": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("length")
                ),

                "Width": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("width")
                ),

                "Height": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("height")
                ),

                "Pack_Quantity": (
                    result.get("attributes", {})
                    .get("normalized", {})
                    .get("pack_quantity")
                ),

                "Identity_Confidence": (
                    result.get("identity", {})
                    .get("confidence")
                ),

                "Attribute_Confidence": (
                    result.get("attributes", {})
                    .get("confidence")
                ),

                "Status": (
                    result.get("attributes", {})
                    .get("status")
                ),

                "Evidence_Count": len(
                    result.get("attributes", {})
                    .get("evidence", [])
                ),
            })

        except Exception as exc:

            results.append({
                "Mfg_Part_Num": row.get("Mfg_Part_Num"),
                "Part_Desc": row.get("Part_Desc"),
                "Status": "error",
                "Evidence_Count": 0,
            })

            print(
                f"[ERROR] Row {index}: {exc}"
            )

    return pd.DataFrame(results)