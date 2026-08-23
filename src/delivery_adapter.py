from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

INTERNAL_FILE = (
    BASE_DIR
    / "data"
    / "output"
    / "final_enriched_products.csv"
)

EXPECTED_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "Unihack_ Expected Output - Delivery Format.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "output"
    / "final_delivery_format.csv"
)


# ============================================================
# HELPERS
# ============================================================

def clean_value(value):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if value in {
        "",
        "nan",
        "NaN",
        "None",
        "none",
        "null",
        "NULL",
    }:
        return pd.NA

    return value


def clean_series(series):

    return series.map(clean_value)


def copy_field(output, target, source, internal):

    if target not in output.columns:
        return

    if source in internal.columns:
        output[target] = clean_series(internal[source])


def copy_first_available(output, target, sources, internal):

    for source in sources:

        if source in internal.columns:

            output[target] = clean_series(
                internal[source]
            )

            return


def split_taxonomy(value):

    if pd.isna(value):
        return []

    parts = [
        x.strip()
        for x in str(value).split(">")
        if x.strip()
    ]

    return parts


# ============================================================
# LOAD
# ============================================================

internal = pd.read_csv(
    INTERNAL_FILE,
    low_memory=False,
)

expected_columns = pd.read_csv(
    EXPECTED_FILE,
    nrows=0,
).columns.tolist()


# ============================================================
# CREATE EXACT DELIVERY STRUCTURE
# ============================================================

delivery = pd.DataFrame(
    pd.NA,
    index=internal.index,
    columns=expected_columns,
)


# ============================================================
# IDENTITY
# ============================================================

copy_first_available(
    delivery,
    "Mfg_Part_Num",
    ["mpn"],
    internal,
)

copy_first_available(
    delivery,
    "PART_NUMBER",
    ["part_number", "PART_NUMBER"],
    internal,
)

# If PART_NUMBER is not available internally,
# use MPN as the stable product identifier.
if (
    "PART_NUMBER" in delivery.columns
    and delivery["PART_NUMBER"].isna().all()
    and "mpn" in internal.columns
):
    delivery["PART_NUMBER"] = clean_series(
        internal["mpn"]
    )


copy_first_available(
    delivery,
    "MANUFACTURER_PART_NUMBER",
    ["mpn"],
    internal,
)

copy_first_available(
    delivery,
    "SKU - MY_PART_NUMBER",
    ["sku", "SKU - MY_PART_NUMBER"],
    internal,
)


# ============================================================
# DESCRIPTION
# ============================================================

description_targets = [
    "Part_Desc",
    "MOBILE_DESC",
    "INVOICE_DESC",
    "SHORT_DESC",
    "LONG_DESC1",
    "RETAIL_DESC",
    "MARKETING_DESCRIPTION",
    "Product Name",
]

for target in description_targets:

    copy_first_available(
        delivery,
        target,
        ["description", "Part_Desc"],
        internal,
    )


# ============================================================
# BRAND
# ============================================================

copy_first_available(
    delivery,
    "E1_Brand",
    ["brand", "E1_Brand"],
    internal,
)

# Do NOT blindly duplicate the resolved brand into
# Unilog_Brand / DIB_Brand. Those represent separate
# enrichment sources in the competition schema.

copy_first_available(
    delivery,
    "BRAND_NAME",
    ["brand"],
    internal,
)

copy_first_available(
    delivery,
    "TRADE_NAME",
    ["brand"],
    internal,
)


# ============================================================
# MANUFACTURER
# ============================================================

copy_first_available(
    delivery,
    "Part_Manuf",
    ["manufacturer", "Part_Manuf"],
    internal,
)

copy_first_available(
    delivery,
    "MANUFACTURER_NAME",
    ["manufacturer", "MANUFACTURER_NAME"],
    internal,
)


# ============================================================
# PRODUCT TYPE
# ============================================================

if "product_type" in internal.columns:

    delivery["Product Name"] = clean_series(
        internal["description"]
    )

    # Product type is useful as the competition Class
    # when no explicit taxonomy hierarchy is available.
    if "Class" in delivery.columns:

        delivery["Class"] = clean_series(
            internal["product_type"]
        )


# ============================================================
# TAXONOMY
# ============================================================

# Search for an already-produced taxonomy CSV.
taxonomy_file = None

for candidate in (
    BASE_DIR / "data" / "output"
).glob("*.csv"):

    if candidate.name == OUTPUT_FILE.name:
        continue

    try:

        candidate_columns = pd.read_csv(
            candidate,
            nrows=0,
        ).columns.tolist()

        if (
            "taxonomy" in candidate_columns
            and (
                "mpn" in candidate_columns
                or "Mfg_Part_Num" in candidate_columns
            )
        ):
            taxonomy_file = candidate
            break

    except Exception:
        continue


if taxonomy_file is not None:

    taxonomy = pd.read_csv(
        taxonomy_file,
        low_memory=False,
    )

    id_column = (
        "mpn"
        if "mpn" in taxonomy.columns
        else "Mfg_Part_Num"
    )

    taxonomy = taxonomy[
        [id_column, "taxonomy"]
    ].copy()

    taxonomy = taxonomy.rename(
        columns={
            id_column: "mpn"
        }
    )

    taxonomy["mpn"] = (
        taxonomy["mpn"]
        .astype(str)
        .str.strip()
    )

    internal["_adapter_mpn"] = (
        internal["mpn"]
        .astype(str)
        .str.strip()
    )

    taxonomy["taxonomy"] = (
        taxonomy["taxonomy"]
        .astype("string")
        .str.strip()
    )

    taxonomy_lookup = dict(
        zip(
            taxonomy["mpn"],
            taxonomy["taxonomy"],
        )
    )

    taxonomy_values = (
        internal["_adapter_mpn"]
        .map(taxonomy_lookup)
    )

    if "Classpath" in delivery.columns:

        delivery["Classpath"] = taxonomy_values

    if (
        "Dept" in delivery.columns
        or "Class" in delivery.columns
        or "Fine" in delivery.columns
    ):

        split_values = taxonomy_values.map(
            split_taxonomy
        )

        if "Dept" in delivery.columns:

            delivery["Dept"] = split_values.map(
                lambda x: x[0]
                if len(x) > 0
                else pd.NA
            )

        if "Class" in delivery.columns:

            delivery["Class"] = split_values.map(
                lambda x: x[1]
                if len(x) > 1
                else (
                    x[0]
                    if len(x) == 1
                    else pd.NA
                )
            )

        if "Fine" in delivery.columns:

            delivery["Fine"] = split_values.map(
                lambda x: x[2]
                if len(x) > 2
                else pd.NA
            )


# ============================================================
# NUMERIC / PHYSICAL ATTRIBUTES
# ============================================================

physical_mapping = {
    "diameter": "DIAMETER",
    "thickness": "THICKNESS",
    "arbor": "ARBOR",
    "length": "LENGTH",
    "width": "WIDTH",
    "height": "HEIGHT",
    "pack_quantity": "Selling Qty",
}

for source, target in physical_mapping.items():

    if (
        source in internal.columns
        and target in delivery.columns
    ):

        delivery[target] = internal[source]


# ============================================================
# ATTRIBUTE SLOTS
# ============================================================

attribute_sources = [
    ("Diameter", "diameter"),
    ("Thickness", "thickness"),
    ("Arbor", "arbor"),
    ("Length", "length"),
    ("Width", "width"),
    ("Height", "height"),
    ("Pack Quantity", "pack_quantity"),
]

slot = 1

for label, source in attribute_sources:

    if source not in internal.columns:
        continue

    if slot > 50:
        break

    label_column = (
        f"ATTRIBUTE_LABEL {slot}"
    )

    value_column = (
        f"ATTRIBUTE_VALUE {slot}"
    )

    uom_column = (
        f"ATTRIBUTE_UOM {slot}"
    )

    if label_column in delivery.columns:

        values = internal[source].map(
            clean_value
        )

        delivery.loc[
            values.notna(),
            label_column,
        ] = label

        delivery.loc[
            values.notna(),
            value_column,
        ] = values

    # Do not invent units when the internal
    # enrichment layer did not establish one.

    slot += 1


# ============================================================
# SEARCH / EVIDENCE INFORMATION
# ============================================================

if "ITEM_FEATURES_1" in delivery.columns:

    if "search_text" in internal.columns:

        delivery["ITEM_FEATURES_1"] = (
            clean_series(
                internal["search_text"]
            )
        )

    elif "description" in internal.columns:

        delivery["ITEM_FEATURES_1"] = (
            clean_series(
                internal["description"]
            )
        )


# ============================================================
# FINAL CLEANUP
# ============================================================

delivery = delivery[
    expected_columns
]


# Ensure no accidental index column
delivery = delivery.reset_index(
    drop=True
)


# ============================================================
# VALIDATION
# ============================================================

assert list(
    delivery.columns
) == expected_columns

assert len(
    delivery.columns
) == 252

assert delivery.columns.is_unique

assert len(
    delivery
) == len(
    internal
)


# ============================================================
# WRITE
# ============================================================

delivery.to_csv(
    OUTPUT_FILE,
    index=False,
)


# ============================================================
# REPORT
# ============================================================

print("=" * 70)
print("COMPETITION DELIVERY ADAPTER")
print("=" * 70)

print(
    "INPUT ROWS:",
    len(internal)
)

print(
    "OUTPUT ROWS:",
    len(delivery)
)

print(
    "OUTPUT COLUMNS:",
    len(delivery.columns)
)

print(
    "OUTPUT:",
    OUTPUT_FILE
)

print()
print("SEMANTIC FIELD CHECK")
print("-" * 70)

preview_columns = [
    "PART_NUMBER",
    "Mfg_Part_Num",
    "Part_Desc",
    "E1_Brand",
    "Part_Manuf",
    "MANUFACTURER_NAME",
    "BRAND_NAME",
    "MANUFACTURER_PART_NUMBER",
    "Classpath",
    "Class",
    "LENGTH",
    "WIDTH",
    "HEIGHT",
    "Selling Qty",
]

preview_columns = [
    c
    for c in preview_columns
    if c in delivery.columns
]

print(
    delivery[
        preview_columns
    ].head(5).to_string(
        index=False
    )
)

print()
print("SCHEMA CHECK: PASS")
print("SEMANTIC MAPPING: COMPLETE")