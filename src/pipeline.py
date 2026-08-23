from .cleaner import clean_product_row
from .identity import build_identity
from .brand_resolver import resolve_brand
from .entity_resolver import resolve_manufacturer
from .attributes import AttributeEnricher
import pandas as pd

def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # Example enrichment logic
    df["row_count"] = range(1, len(df) + 1)
    # Add your actual transformation steps here
    return df

def enrich_product(row, attribute_enricher=None, comapny_lov=None):
    """
    Run the complete product enrichment pipeline.

    Flow:
        raw row
            ↓
        cleaning
            ↓
        identity extraction
            ↓
        brand resolution
            ↓
        manufacturer resolution
            ↓
        attribute extraction
            ↓
        normalized attributes
    """

    # ---------------------------------------------------------
    # 1. CLEAN
    # ---------------------------------------------------------

    cleaned = clean_product_row(row)

    # ---------------------------------------------------------
    # 2. IDENTITY
    # ---------------------------------------------------------

    identity = build_identity(cleaned)

    # ---------------------------------------------------------
    # 3. BRAND
    # ---------------------------------------------------------

    brand_result = resolve_brand(cleaned)

    # ---------------------------------------------------------
    # 4. MANUFACTURER
    # ---------------------------------------------------------

    manufacturer_result = resolve_manufacturer(
        cleaned.get("manufacturer")
    )

    # ---------------------------------------------------------
    # 5. ATTRIBUTE ENRICHMENT
    # ---------------------------------------------------------

    if attribute_enricher is None:
        attribute_enricher = AttributeEnricher()

    attribute_text = " ".join(
        [
            str(cleaned.get("mpn") or ""),
            str(cleaned.get("part_description") or ""),
        ]
    ).strip()

    attribute_result = attribute_enricher.enrich(
        attribute_text
    )

    # ---------------------------------------------------------
    # 6. FINAL RESULT
    # ---------------------------------------------------------

    return {
        "identity": identity,
        "brand": brand_result,
        "manufacturer": manufacturer_result,
        "attributes": attribute_result,
    }