from typing import Any


def build_identity(row: Any) -> dict[str, Any]:

    # Accept either a raw pandas Series/dict or an already-cleaned record.
    if "Mfg_Part_Num" in row:
        from .cleaner import clean_product_row
        cleaned = clean_product_row(row)
    else:
        cleaned = row

    mpn = cleaned.get("mpn")
    description = cleaned.get("part_description")
    manufacturer = cleaned.get("manufacturer")

    brands = []

    for key in ["e1_brand", "unilog_brand", "dib_brand"]:
        value = cleaned.get(key)

        if value:
            brands.append(value)

    # Remove the supplier code from:
    # "Milwaukee Accessory (4031)"
    manufacturer_candidate = manufacturer

    if manufacturer_candidate:
        manufacturer_candidate = manufacturer_candidate.rsplit("(", 1)[0].strip()

     # Pick one brand candidate (ignore placeholders like "-- Unbranded --")
    brand_candidate = None
    for b in brands:
        if not b.startswith("--"):
            brand_candidate = b
            break

    identity_query = " ".join(
        [x for x in [mpn, manufacturer_candidate, brand_candidate] if x]
    )

    return {
        "mpn": mpn,
        "manufacturer": manufacturer,
        "manufacturer_candidate": manufacturer_candidate,
        "brand_candidate": brand_candidate,
        "identity_query": identity_query,
        "brands": brands,
        "description": description,
    }