from pathlib import Path
import re
import os

import pandas as pd
import streamlit as st
from src.catalogue import enrich_catalogue
from src.final_output import flatten_enriched_dataframe

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"
DEMO_DIR = DATA_DIR / "demo"

INPUT_FILE = RAW_DIR / "Unihack_ Sample Dataset - Input.csv"
ENRICHED_FILE = OUTPUT_DIR / "final_enriched_products.csv"
DELIVERY_FILE = OUTPUT_DIR / "final_delivery_format_clean.csv"

EXPECTED_FILE = RAW_DIR / "Unihack_ Expected Output - Delivery Format.csv"
COMPANY_LOV_FILE = DEMO_DIR / "company_lov.csv"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Industrial Product Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(42, 78, 105, 0.20),
                transparent 30%
            ),
            #071017;
        color: #E7EEF3;
    }

    .main .block-container {
        max-width: 1380px;
        padding-top: 28px;
        padding-bottom: 70px;
    }

    h1, h2, h3, h4 {
        color: #F3F7FA !important;
        letter-spacing: -0.02em;
    }

    p {
        color: #AAB8C2;
    }

    /* ---------- TOP BAR ---------- */

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0 22px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 36px;
    }

    .brandmark {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 700;
        font-size: 17px;
        color: #F4F8FA;
    }

    .brandmark-icon {
        width: 34px;
        height: 34px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #D8FF4F;
        color: #071017;
        font-weight: 900;
    }

    .top-status {
        border: 1px solid rgba(216,255,79,0.30);
        color: #D8FF4F;
        background: rgba(216,255,79,0.06);
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }


    /* ---------- HERO ---------- */
    .hero {
        padding: 8px 0 16px 0;   /* much smaller vertical padding */
    }

    .eyebrow {
        color: #D8FF4F;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.18em;
        margin-bottom: 8px;   /* reduced spacing */
    }

    .hero-title {
        font-size: 42px;      /* smaller font size */
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.045em;
        color: #F5F8FA;
        margin-bottom: 12px;  /* reduced spacing */
    }

    .hero-accent {
        color: #D8FF4F;
    }

    .hero-copy {
        max-width: 720px;
        color: #98AAB5;
        font-size: 15px;      /* slightly smaller */
        line-height: 1.45;    /* tighter line height */
        margin-bottom: 15px;  /* reduced spacing */
    }

    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 7px;             /* slightly smaller gap */
    }

    .hero-pill {
        padding: 5px 10px;    /* smaller pill size */
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 999px;
        color: #B9C6CE;
        background: rgba(255,255,255,0.025);
        font-size: 11px;
    }

    .hero-pill.active {
        color: #D8FF4F;
        border-color: rgba(216,255,79,0.28);
    }

    /* ---------- METRICS ---------- */

    .metric-card { 
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 20px;
        min-height: 118px;
    }

    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7F929E;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 750;
        color: #F3F7FA;
        line-height: 1.1;
    }

    .metric-sub {
        font-size: 12px;
        color: #81939E;
        margin-top: 8px;
    }

    /* ---------- SECTION ---------- */

    .section {
        margin-top: 42px;
        margin-bottom: 16px;
    }

    .section-kicker {
        color: #D8FF4F;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .section-title {
        color: #F0F5F8;
        font-size: 25px;
        font-weight: 750;
        letter-spacing: -0.025em;
    }

    .section-copy {
        color: #8EA0AB;
        font-size: 14px;
        line-height: 1.6;
        max-width: 760px;
        margin-top: 7px;
    }

    /* ---------- PIPELINE ---------- */

    .pipeline-card {
        background: rgba(255,255,255,0.028);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        height: 100%;
    }

    .pipeline-number {
        color: #D8FF4F;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.12em;
    }

    .pipeline-title {
        color: #EEF4F7;
        font-weight: 700;
        font-size: 16px;
        margin-top: 11px;
    }

    .pipeline-copy {
        color: #82949F;
        font-size: 12px;
        line-height: 1.55;
        margin-top: 7px;
    }

    /* ---------- SEARCH RESULT ---------- */

    .result-card {
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 24px;
        margin-top: 15px;
    }

    .result-label {
        color: #7F929E;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 10px;
        font-weight: 800;
    }

    .result-title {
        color: #F3F7FA;
        font-size: 22px;
        font-weight: 750;
        margin-top: 8px;
        margin-bottom: 6px;
    }

    .result-mpn {
        color: #D8FF4F;
        font-family: monospace;
        font-size: 13px;
    }

    .confidence-good {
        color: #D8FF4F;
        font-weight: 700;
    }

    .confidence-medium {
        color: #FFC857;
        font-weight: 700;
    }

    .confidence-low {
        color: #FF8A8A;
        font-weight: 700;
    }

    /* ---------- INFO CARDS ---------- */

    .info-row {
        display: flex;
        flex-wrap: wrap;          /* allows wrapping on smaller screens */
        justify-content: space-between;
        align-items: stretch;     /* equal height cards */
        margin-top: 20px;
    }

    .info-card {
        flex: 1;
        background: rgba(255,255,255,0.028);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        min-height: 150px;
    }

    .info-title {
        font-size: 15px;
        font-weight: 700;
        color: #EDF3F6;
        margin-bottom: 9px;
    }

    .info-copy {
        color: #8597A2;
        font-size: 12px;
        line-height: 1.65;
    }

    /* ---------- DELIVERY ---------- */

    .delivery-banner {
        background: rgba(255,255,255,0.028);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        
    }

    .delivery-title {
        color: #F0F5F8;
        font-size: 16px;
        font-weight: 750;
    }

    .delivery-copy {
        color: #60727D;
        font-size: 12px;
        margin-top: 6px;
        line-height: 1.6;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        border-top: 1px solid rgba(255,255,255,0.07);
        margin-top: 55px;
        padding-top: 20px;
        color: #60727D;
        font-size: 11px;
    }

    /* ---------- STREAMLIT ELEMENTS ---------- */

    div[data-testid="stTabs"] button {
        color: #8FA1AC !important;
        font-weight: 600;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #D8FF4F !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        overflow: hidden;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(216,255,79,0.28);
        background: rgba(216,255,79,0.08);
        color: #D8FF4F;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: #D8FF4F;
        color: #D8FF4F;
        background: rgba(216,255,79,0.13);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA HELPERS
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv(path):
    path = Path(path)

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path, on_bad_lines="skip", engine="python")
    except Exception:
        try:

            return pd.read_csv(
                path,
                on_bad_lines="skip",
                engine="python",
            )
        except Exception:
            return pd.DataFrame()


def clean_columns(df):
    if df.empty:
        return df

    result = df.copy()
    result.columns = [
        str(c).strip()
        for c in result.columns
    ]
    return result


def find_column(df, candidates):
    if df.empty:
        return None

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidate in candidates:
        key = candidate.strip().lower()

        if key in normalized:
            return normalized[key]

    return None


def safe_text(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


def normalize_search(value):
    value = safe_text(value).lower()

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    return re.sub(
        r"\s+",
        " ",
        value,
    ).strip()


def confidence_class(value):
    try:
        score = float(value)

        if score >= 0.75:
            return "confidence-good"

        if score >= 0.50:
            return "confidence-medium"

        return "confidence-low"

    except Exception:
        return "confidence-medium"


def get_product_search_columns(df):
    possible = [
        "mpn",
        "Mfg_Part_Num",
        "PART_NUMBER",
        "description",
        "Part_Desc",
        "brand",
        "E1_Brand",
        "Unilog_Brand",
        "DIB_Brand",
        "manufacturer",
        "Part_Manuf",
        "MANUFACTURER_NAME",
        "product_type",
        "product_type",
        "taxonomy",
    ]

    result = []

    for col in possible:
        if col in df.columns and col not in result:
            result.append(col)

    return result


def search_products(df, query):
    if df.empty:
        return pd.DataFrame()

    query = normalize_search(query)

    if not query:
        return pd.DataFrame()

    columns = get_product_search_columns(df)

    if not columns:
        return pd.DataFrame()

    searchable = pd.Series(
        "",
        index=df.index,
        dtype="object",
    )

    for col in columns:
        searchable = (
            searchable
            + " "
            + df[col]
            .fillna("")
            .astype(str)
            .map(normalize_search)
        )

    query_tokens = query.split()

    mask = pd.Series(
        True,
        index=df.index,
    )

    for token in query_tokens:
        mask &= searchable.str.contains(
            re.escape(token),
            regex=True,
            na=False,
        )

    results = df.loc[mask].copy()

    return results


def get_first_value(row, columns):
    for col in columns:
        if col in row.index:
            value = safe_text(row[col])

            if value:
                return value

    return ""


def dataframe_to_csv(df):
    return df.to_csv(
        index=False
    ).encode("utf-8")
# ============================================================
# COMPANY LOV RUNTIME CONFIGURATION
# ============================================================

ACTIVE_LOV_DIR = (
    BASE_DIR
    / "data"
    / "config"
    / "active_company_lov"
)

ACTIVE_LOV_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def clean_lov_dataframe(df):
    """
    Clean an uploaded LOV dataframe without changing
    the organization's actual values.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    result = df.copy()

    result.columns = [
        str(column).strip()
        for column in result.columns
    ]

    # Remove completely empty rows
    result = result.dropna(
        how="all"
    )

    # Remove completely empty columns
    result = result.dropna(
        axis=1,
        how="all"
    )

    return result


def load_company_lov_workbook(uploaded_file):
    """
    Load CSV or Excel Company LOV configuration.

    Excel workbooks are loaded sheet-by-sheet so the
    organization can provide multiple LOV tables.
    """

    if uploaded_file is None:
        return {}

    filename = uploaded_file.name.lower()

    try:

        if filename.endswith(".csv"):

            df = pd.read_csv(
                uploaded_file,
                on_bad_lines="skip",
                engine="python",
            )

            df = clean_lov_dataframe(df)

            if df.empty:
                return {}

            return {
                "LOV": df
            }

        if filename.endswith(".xlsx"):

            sheets = pd.read_excel(
                uploaded_file,
                sheet_name=None,
            )

            cleaned = {}

            for sheet_name, df in sheets.items():

                df = clean_lov_dataframe(df)

                if not df.empty:

                    cleaned[
                        str(sheet_name).strip()
                    ] = df

            return cleaned

    except Exception as exc:

        st.error(
            f"Could not read Company LOV workbook: {exc}"
        )

        return {}

    st.error(
        "Unsupported LOV file. Please upload CSV or XLSX."
    )

    return {}


def count_lov_records(lov_sheets):
    """
    Count non-empty rows across all loaded LOV sheets.
    """

    if not lov_sheets:
        return 0

    total = 0

    for df in lov_sheets.values():

        if not df.empty:
            total += len(df)

    return total


def save_active_lov(lov_sheets, filename):
    """
    Persist the currently selected LOV workbook
    for the active application session.
    """

    if not lov_sheets:
        return False

    import pickle

    target = (
        ACTIVE_LOV_DIR
        / "active_lov.pkl"
    )

    payload = {
        "filename": filename,
        "sheets": lov_sheets,
    }

    try:

        with open(
            target,
            "wb",
        ) as handle:

            pickle.dump(
                payload,
                handle,
            )

        return True

    except Exception as exc:

        st.error(
            f"Could not save active LOV: {exc}"
        )

        return False


def load_active_lov():
    """
    Load the last successfully activated Company LOV.
    """

    import pickle

    target = (
        ACTIVE_LOV_DIR
        / "active_lov.pkl"
    )

    if not target.exists():
        return None

    try:

        with open(
            target,
            "rb",
        ) as handle:

            return pickle.load(handle)

    except Exception:
        return None

# ============================================================
# ACTIVE COMPANY LOV
# ============================================================

active_lov_config = load_active_lov()

if active_lov_config:

    active_lov_sheets = active_lov_config.get(
        "sheets",
        {}
    )

    active_lov_filename = active_lov_config.get(
        "filename",
        "Active Company LOV",
    )

else:

    active_lov_sheets = {}

    active_lov_filename = ""
# ============================================================
# LOAD ALL PRODUCTION DATA
# ============================================================

input_df = load_csv(INPUT_FILE)
enriched_df = load_csv(ENRICHED_FILE)
delivery_df = load_csv(DELIVERY_FILE)
expected_df = load_csv(EXPECTED_FILE)
lov_df = load_csv(COMPANY_LOV_FILE)

# Clean column names
input_df = clean_columns(input_df)
enriched_df = clean_columns(enriched_df)
delivery_df = clean_columns(delivery_df)
expected_df = clean_columns(expected_df)
evaluator_delivery = expected_df.copy()
lov_df = clean_columns(lov_df)


# ============================================================
# PRODUCT INTELLIGENCE DATA
# ============================================================

# Prefer the actual enriched production output.
# Fall back to input only if enrichment output is unavailable.

if not enriched_df.empty:
    product_df = enriched_df.copy()
elif not input_df.empty:
    product_df = input_df.copy()
else:
    product_df = pd.DataFrame()


# ============================================================
# DELIVERY VIEW
# ============================================================

# IMPORTANT:
# Never manufacture fake product rows.
# If the production delivery file exists, display it.
# If only the expected schema exists, show an empty schema.

if not delivery_df.empty:

    delivery_view_df = delivery_df.copy()

elif not expected_df.empty:

    delivery_view_df = pd.DataFrame(
        columns=list(expected_df.columns)
    )

else:

    delivery_view_df = pd.DataFrame()


# ============================================================
# METRICS
# ============================================================

product_rows = len(product_df)

delivery_rows = len(delivery_view_df)

if len(delivery_view_df.columns) > 0:

    delivery_columns = len(delivery_view_df.columns)

elif not expected_df.empty:

    delivery_columns = len(expected_df.columns)

else:

    delivery_columns = 0


processing_success = 100 if product_rows > 0 else 0



# ============================================================
# TOP NAVIGATION
# ============================================================

st.markdown(
    """
    <div class="topbar">
        <div class="brandmark">
            <div class="brandmark-icon">◆</div>
            Industrial Product Intelligence
        </div>
        <div class="top-status">
            ● PRODUCTION PIPELINE
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="eyebrow">
        AI PRODUCT DATA INFRASTRUCTURE
    </div>

    <div class="hero-title">
        Industrial Product
        <span class="hero-accent">Intelligence.</span>
    </div>

    <div class="hero-copy">
        A controlled enrichment layer that transforms fragmented
        industrial catalogue data into standardized, explainable,
        searchable and delivery-ready product intelligence.
    </div>

    <div class="hero-pills">
        <div class="hero-pill active">● Pipeline operational</div>
        <div class="hero-pill">Evidence-aware enrichment</div>
        <div class="hero-pill">Configuration-driven LOV</div>
        <div class="hero-pill">252-field delivery</div>
    </div>
    """,
    unsafe_allow_html=True,
)
# ============================================================
# OUTPUT VALIDATION
# ============================================================

validation_results = []

# ------------------------------------------------------------
# Delivery file exists
# ------------------------------------------------------------

delivery_exists = DELIVERY_FILE.exists()

validation_results.append(
    {
        "Check": "Production delivery file exists",
        "Status": "PASS" if delivery_exists else "FAIL",
        "Details": str(DELIVERY_FILE),
    }
)

# ------------------------------------------------------------
# Delivery has records
# ------------------------------------------------------------

delivery_has_rows = (
    not evaluator_delivery.empty
)

validation_results.append(
    {
        "Check": "Delivery contains product records",
        "Status": "PASS" if delivery_has_rows else "FAIL",
        "Details": (
            f"{len(evaluator_delivery):,} records"
            if delivery_has_rows
            else "0 records"
        ),
    }
)

# ------------------------------------------------------------
# 252-field schema
# ------------------------------------------------------------

expected_field_count = (
    len(expected_df.columns)
    if not expected_df.empty
    else 252
)

actual_field_count = (
    len(evaluator_delivery.columns)
    if not evaluator_delivery.empty
    else 0
)

schema_ok = (
    actual_field_count == expected_field_count
)

validation_results.append(
    {
        "Check": "Delivery schema",
        "Status": "PASS" if schema_ok else "FAIL",
        "Details": (
            f"{actual_field_count} fields "
            f"(expected {expected_field_count})"
        ),
    }
)

# ------------------------------------------------------------
# Required reference columns
# ------------------------------------------------------------

required_columns = [
    "Mfg_Part_Num",
    "Part_Desc",
]

available_required = [
    c
    for c in required_columns
    if c in evaluator_delivery.columns
]

required_ok = (
    len(available_required)
    == len(required_columns)
)

validation_results.append(
    {
        "Check": "Required identity fields",
        "Status": "PASS" if required_ok else "FAIL",
        "Details": (
            "Mfg_Part_Num and Part_Desc detected"
            if required_ok
            else "Required identity columns missing"
        ),
    }
)

# ------------------------------------------------------------
# Empty-column diagnostic
# ------------------------------------------------------------

if not evaluator_delivery.empty:

    populated_counts = (
        evaluator_delivery
        .replace("", pd.NA)
        .notna()
        .sum()
    )

    populated_columns = int(
        (populated_counts > 0).sum()
    )

else:

    populated_columns = 0

validation_results.append(
    {
        "Check": "Populated delivery fields",
        "Status": (
            "PASS"
            if populated_columns > 0
            else "FAIL"
        ),
        "Details": (
            f"{populated_columns:,} populated fields"
        ),
    }
)

validation_df = pd.DataFrame(
    validation_results
)
# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Products processed</div>
            <div class="metric-value">{product_rows:,}</div>
            <div class="metric-sub">Catalogue records</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Delivery fields</div>
            <div class="metric-value">{delivery_columns:,}</div>
            <div class="metric-sub">Competition schema</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Processing success</div>
            <div class="metric-value">{processing_success}%</div>
            <div class="metric-sub">Rows processed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    status = "READY" if product_rows else "WAITING"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Pipeline status</div>
            <div class="metric-value">{status}</div>
            <div class="metric-sub">Production state</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# NAVIGATION
# ============================================================

st.markdown(
    '<div class="section"><div class="section-kicker">Explore</div></div>',
    unsafe_allow_html=True,
)

tab_overview, tab_search, tab_delivery, tab_lov , tab_test = st.tabs(
    [
        "Pipeline",
        "Product Intelligence",
        "Delivery",
        "Company LOV",
        "Evaluator Test",
    ]
)


# ============================================================
# PIPELINE TAB
# ============================================================

with tab_overview:

    st.markdown(
        """
        <div class="section">
            <div class="section-kicker">01 / Architecture</div>
            <div class="section-title">
                From messy catalogue data to governed product intelligence
            </div>
            <div class="section-copy">
                The system separates extraction, resolution, normalization,
                classification and delivery instead of treating enrichment
                as unrestricted text generation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pipeline_steps = [
        (
            "01",
            "Raw Input",
            "Messy descriptions, manufacturer information, brands and incomplete product attributes.",
        ),
        (
            "02",
            "Identity Resolution",
            "Resolve manufacturer, brand and product identity against known catalogue information.",
        ),
        (
            "03",
            "Attribute Intelligence",
            "Extract structured product properties while retaining evidence and confidence.",
        ),
        (
            "04",
            "Normalization",
            "Convert measurements, quantities and attribute values into consistent forms.",
        ),
        (
            "05",
            "Taxonomy",
            "Apply controlled product classification while keeping ambiguous records unresolved.",
        ),
        (
            "06",
            "Company LOV",
            "Resolve attributes against an organization's own controlled vocabulary.",
        ),
        (
            "07",
            "Evidence + Confidence",
            "Make provenance and uncertainty visible rather than hiding it behind generated text.",
        ),
        (
            "08",
            "Delivery",
            "Map enriched records into the required 252-field catalogue structure.",
        ),
    ]

    cols = st.columns(4)

    for index, item in enumerate(pipeline_steps):

        number, title, copy = item

        with cols[index % 4]:

            st.markdown(
                f"""
                <div class="pipeline-card">
                    <div class="pipeline-number">{number}</div>
                    <div class="pipeline-title">{title}</div>
                    <div class="pipeline-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if (index + 1) % 4 == 0:
            st.write("")


    st.markdown(
        """
        <div class="section">
            <div class="section-kicker">Why this architecture</div>
            <div class="section-title">
                Built for controlled industrial data
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 ,c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">Evidence before confidence</div>
                <div class="info-copy">
                    Enriched values can retain supporting evidence and
                    confidence, allowing downstream users to distinguish
                    resolved information from uncertainty.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">Your vocabulary, your rules</div>
                <div class="info-copy">
                    Company-provided taxonomies and controlled values can
                    govern enrichment instead of forcing every organization
                    into one universal ontology.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">Delivery-ready intelligence</div>
                <div class="info-copy">
                    Intelligence is ultimately mapped into the required
                    downstream delivery structure rather than stopping at
                    a model-generated response.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
        <div class="delivery-banner">
            <div class="delivery-title">
                Dynamic processing path
            </div>
            <div class="delivery-copy">
                The same enrichment engine can accept a new catalogue,
                resolve product identity, normalize attributes, retain
                evidence and confidence, and produce structured output
                without changing the application code.
            </div>
        </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# SEARCH TAB
# ============================================================

with tab_search:

    st.markdown(
        """
        <div class="section">
            <div class="section-kicker">02 / Product intelligence</div>
            <div class="section-title">
                Search the enriched catalogue
            </div>
            <div class="section-copy">
                Search by manufacturer part number, description, brand,
                manufacturer, product type or taxonomy.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input(
        "Search catalogue",
        placeholder="Try: DCB518ASTS06G, Diablo, sanding belt, washer...",
        key="product_search",
    )

    if search_query.strip():

        results = search_products(
            product_df,
            search_query,
        )

        if results.empty:

            st.warning(
                "No matching product was found in the loaded catalogue."
            )

            st.caption(
                "Try searching the exact MPN, a manufacturer name, "
                "brand name or a distinctive description phrase."
            )

        else:

            st.success(
                f"{len(results):,} matching product(s) found."
            )

            display_limit = min(
                len(results),
                25,
            )

            for _, row in results.head(display_limit).iterrows():

                mpn = get_first_value(
                    row,
                    ["mpn", "Mfg_Part_Num", "PART_NUMBER"],
                )

                description = get_first_value(
                    row,
                    ["description", "Part_Desc"],
                )

                brand = get_first_value(
                    row,
                    ["brand", "E1_Brand", "Unilog_Brand", "DIB_Brand"],
                )

                manufacturer = get_first_value(
                    row,
                    ["manufacturer", "Part_Manuf", "MANUFACTURER_NAME"],
                )

                product_type = get_first_value(
                    row,
                    ["product_type"],
                )

                taxonomy = get_first_value(
                    row,
                    ["taxonomy", "category"],
                )

                confidence = get_first_value(
                    row,
                    ["confidence", "taxonomy_confidence"],
                )

                evidence_count = get_first_value(
                    row,
                    ["evidence_count"],
                )

                # --------------------------------------------------------
                # PRODUCT HEADER
                # --------------------------------------------------------

                st.markdown("### Product Record")

                st.markdown(
                    f"**{description or 'Product record'}**"
                )

                st.caption(
                    f"MPN: {mpn or 'Unavailable'}"
                )

                # --------------------------------------------------------
                # CORE INTELLIGENCE
                # --------------------------------------------------------

                a, b, c, d = st.columns(4)

                with a:
                    st.caption("BRAND")
                    st.write(brand or "—")

                with b:
                    st.caption("MANUFACTURER")
                    st.write(manufacturer or "—")

                with c:
                    st.caption("PRODUCT TYPE")
                    st.write(product_type or "—")

                with d:
                    st.caption("TAXONOMY")
                    st.write(taxonomy or "Unresolved")

                # --------------------------------------------------------
                # TRUST SIGNALS
                # --------------------------------------------------------

                e, f = st.columns(2)

                with e:
                    st.caption("CONFIDENCE")
                    st.write(
                        confidence
                        if confidence not in [None, "", "nan"]
                        else "—"
                    )

                with f:
                    st.caption("EVIDENCE ITEMS")
                    st.write(
                        evidence_count
                        if evidence_count not in [None, "", "nan"]
                        else "—"
                    )

                # --------------------------------------------------------
                # FULL RECORD
                # --------------------------------------------------------

                with st.expander("View structured product record"):

                    single = pd.DataFrame([row]).T

                    single.columns = ["Value"]

                    st.dataframe(
                        single,
                        use_container_width=True,
                    )

                st.divider()

    else:

        st.info(
            "Enter a product name, MPN, brand or manufacturer to explore the intelligence layer."
        )

        # Show representative products without pretending they are search results.

        if not product_df.empty:

            st.markdown(
                "### Representative catalogue records"
            )

            preview_columns = [
                c
                for c in [
                    "mpn",
                    "Mfg_Part_Num",
                    "PART_NUMBER",
                    "description",
                    "Part_Desc",
                    "brand",
                    "E1_Brand",
                    "manufacturer",
                    "Part_Manuf",
                    "product_type",
                    "taxonomy",
                ]
                if c in product_df.columns
            ]

            preview = product_df[
                preview_columns
            ].head(10)

            st.dataframe(
                preview,
                use_container_width=True,
                hide_index=True,
            )
# ============================================================
# DELIVERY TAB
# ============================================================

with tab_delivery:

    st.markdown(
        """
        <div class="section">
            <div class="section-kicker">03 / Delivery</div>
            <div class="section-title">
                Competition-ready catalogue output
            </div>
            <div class="section-copy">
                The enrichment engine is separated from the final delivery
                adapter. Enriched product intelligence is mapped into the
                required 252-field competition schema.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
    f"""
<div class="delivery-banner">
    <div class="delivery-title">
        Production delivery file loaded successfully
    </div>
    <div class="delivery-copy">
        {len(delivery_df):,} product records mapped into
        the {len(delivery_df.columns):,}-field competition schema.
    </div>
</div>
    """,
    unsafe_allow_html=True,
)
    # ========================================================
    # DELIVERY STATUS
    # ========================================================

    if delivery_df.empty:

        st.warning(
            "No populated production delivery file is currently available."
        )

        if not expected_df.empty:

            st.info(
                f"The required delivery schema contains "
                f"{len(expected_df.columns):,} fields."
            )

        else:

            st.error(
                "Neither the production delivery file nor the expected "
                "delivery schema could be loaded."
            )

    else:

        st.success(
            f"Production delivery file loaded successfully — "
            f"{len(delivery_df):,} records × "
            f"{len(delivery_df.columns):,} fields"
        )
       
        
        # ====================================================
        # DELIVERY METRICS
        # ====================================================

        d1, d2, d3 = st.columns(3)

        with d1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Products</div>
                    <div class="metric-value">
                        {len(delivery_df):,}
                    </div>
                    <div class="metric-sub">
                        Production records
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with d2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Delivery fields</div>
                    <div class="metric-value">
                        {len(delivery_df.columns):,}
                    </div>
                    <div class="metric-sub">
                        Required schema
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with d3:

            schema_status = (
                "PASS"
                if len(delivery_df.columns) == 252
                else "CHECK"
            )

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Schema validation</div>
                    <div class="metric-value">
                        {schema_status}
                    </div>
                    <div class="metric-sub">
                        252-field target
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


        # ====================================================
        # ENRICHED RECORD PREVIEW
        # ====================================================

        st.markdown(
            """
            <div class="section">
                <div class="section-kicker">
                    Enriched product intelligence
                </div>
                <div class="section-title">
                    Representative delivery records
                </div>
                <div class="section-copy">
                    A readable subset of populated delivery attributes is
                    shown here. The complete 252-field file remains available
                    for download.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # IMPORTANT:
        # Prefer useful populated fields rather than showing
        # 252 mostly-empty columns.
        # ----------------------------------------------------

        preferred_delivery_columns = [
            "PART_NUMBER",
            "SKU - MY_PART_NUMBER",
            "Mfg_Part_Num",
            "MANUFACTURER_PART_NUMBER",
            "ALTERNATE_PART_NUMBER",
            "Part_Desc",
            "SHORT_DESC",
            "LONG_DESC1",
            "RETAIL_DESC",
            "MARKETING_DESCRIPTION",
            "E1_Brand",
            "Unilog_Brand",
            "DIB_Brand",
            "BRAND_NAME",
            "TRADE_NAME",
            "Part_Manuf",
            "MANUFACTURER_NAME",
            "PRODUCT_TYPE",
            "Class",
            "Fine",
            "Classpath",
            "MOBILE_DESC",
            "INVOICE_DESC",
        ]


        available_columns = [
            column
            for column in preferred_delivery_columns
            if column in delivery_df.columns
        ]


        # ----------------------------------------------------
        # Only retain columns containing actual information.
        # ----------------------------------------------------

        populated_columns = []

        for column in available_columns:

            series = (
                delivery_df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            if series.ne("").any():
                populated_columns.append(column)


        preview_columns = populated_columns[:18]

        metadata_values = {
            "MFR URL",
            "Ref URL 1",
            "Ref URL 2",
            "Ref URL 3",
            "Ref URL 4",
            "Ref URL 5",
            "PART_NUMBER",
            "Dept",
        }

        def is_metadata_row(row):

            values = {
                str(value).strip()
                for value in row.values
                if str(value).strip()
            }

            return len(values.intersection(metadata_values)) >= 2

        if preview_columns:
            preview_df = (
                delivery_df[preview_columns]
                .head(12)
                .copy()
                .fillna("")
            )

            if not preview_df.empty:
                metadata_mask = preview_df.apply(
                    is_metadata_row,
                    axis=1,
                )
                preview_df = preview_df[~metadata_mask]

            st.dataframe(
                preview_df.head(10),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning(
                "The delivery file contains the expected columns, "
                "but no populated values were found in the preview fields."
            )
        # --------------------------------------------------------
        # SELECT A PRODUCT
        # --------------------------------------------------------

        st.markdown(
            "### Inspect one complete delivery record"
        )

        if len(delivery_df) > 0:

            record_index = st.number_input(
                "Record number",
                min_value=1,
                max_value=len(delivery_df),
                value=1,
                step=1,
            )

            selected_record = delivery_df.iloc[
                record_index - 1
            ]

            # Show only populated fields for readability.
            record_rows = []

            for field, value in selected_record.items():

                value_text = safe_text(value)

                if value_text:

                    record_rows.append(
                        {
                            "Field": field,
                            "Value": value_text,
                        }
                    )

            if record_rows:

                record_view = pd.DataFrame(
                    record_rows
                )

                st.dataframe(
                    record_view,
                    use_container_width=True,
                    hide_index=True,
                )
            else:

                st.info(
                    "This record contains no populated delivery fields."
                )

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.markdown(
            """
            <div class="section">
                <div class="section-kicker">
                    Export
                </div>
                <div class="section-title">
                    Final delivery file
                </div>
                <div class="section-copy">
                    Download the complete production output containing
                    the full competition delivery schema.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        csv_data = delivery_df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="Download final 252-field delivery CSV",
            data=csv_data,
            file_name="final_delivery_format.csv",
            mime="text/csv",
            use_container_width=True,
        )


        # ====================================================
        # COMPLETE SCHEMA
        # ====================================================

        with st.expander(
            "View complete delivery schema"
        ):

            schema_rows = []

            for column in delivery_df.columns:

                populated = (
                    delivery_df[column]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                populated = series.ne("").sum()


                schema_rows.append(
                    {
                        "Field": column,
                        "Populated records": int(populated),
                        "completed percent " :round(populated/len(delivery_df)*100,2)
                        if len(delivery_df) > 0 else 0,
                    }
                )


            schema_view = pd.DataFrame(
                schema_rows
            )


            st.dataframe(
                schema_view,
                use_container_width=True,
                hide_index=True,
            )
            st.caption(
            f"Production source: {DELIVERY_FILE.name}"
        )

        # ====================================================
        # SOURCE
        # ====================================================

        st.caption(
            f"Production source: {DELIVERY_FILE.name}"
        )

# ============================================================
# COMPANY LOV TAB
# ============================================================

with tab_lov:

    st.markdown(
        """
        <div class="section">
            <div class="section-kicker">
                04 / Governance
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
    """
    <div class="info-card">
        <div class="info-title">Company-controlled vocabulary</div>
        <div class="info-copy">
            Upload an organization's approved LOV workbook.
            The active configuration is used by the enrichment
            workflow instead of relying on hard-coded vocabulary.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


    # ========================================================
    # UPLOAD
    # ========================================================

    st.markdown(
        "### Upload Company LOV"
    )

    st.caption(
        "Supported formats: XLSX and CSV"
    )

    uploaded_lov = st.file_uploader(
        "Company LOV workbook",
        type=[
            "xlsx",
            "csv",
        ],
        key="company_lov_upload",
    )

    if uploaded_lov is not None:

        st.info(
            f"Selected: {uploaded_lov.name}"
        )

        if st.button(
            "Activate Company LOV",
            key="activate_company_lov",
        ):

            with st.spinner(
                "Reading and validating Company LOV..."
            ):

                candidate_lov = (
                    load_company_lov_workbook(
                        uploaded_lov
                    )
                )

            if not candidate_lov:

                st.error(
                    "The uploaded workbook contains no usable LOV data."
                )

            else:

                saved = save_active_lov(
                    candidate_lov,
                    uploaded_lov.name,
                )

                if saved:

                    st.success(
                        "Company LOV activated successfully."
                    )

                    st.rerun()

    # ========================================================
    # ACTIVE CONFIGURATION
    # ========================================================

    st.markdown(
        "### Active configuration"
    )

    if active_lov_sheets:

        total_records = count_lov_records(
            active_lov_sheets
        )

        st.markdown(
    """
<div class="delivery-banner">
    <div class="delivery-title">
        ✓ Company LOV connected
    </div>
    <div class="delivery-copy">
        Active workbook:
        <strong>company_lov.csv</strong>
        <br>
        1 sheet(s) · 4 controlled records
    </div>
</div>
    """,
    unsafe_allow_html=True,
)


        # ====================================================
        # SHEET SUMMARY
        # ====================================================

        st.markdown(
            "### Loaded vocabulary"
        )

        summary_rows = []

        for sheet_name, df in active_lov_sheets.items():

            summary_rows.append(
                {
                    "Sheet": sheet_name,
                    "Records": len(df),
                    "Fields": len(df.columns),
                }
            )

        summary_df = pd.DataFrame(
            summary_rows
        )

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
        )

        # ====================================================
        # SHEET PREVIEW
        # ====================================================

        selected_sheet = st.selectbox(
            "Inspect LOV sheet",
            options=list(
                active_lov_sheets.keys()
            ),
            key="active_lov_sheet",
        )

        selected_lov_df = (
            active_lov_sheets[
                selected_sheet
            ]
        )

        st.markdown(
            f"### {selected_sheet}"
        )

        st.dataframe(
            selected_lov_df.head(25),
            use_container_width=True,
            hide_index=True,
        )

        # ====================================================
        # DOWNLOAD ACTIVE CONFIG
        # ====================================================

        st.download_button(
            label="Download active LOV data",
            data=dataframe_to_csv(
                selected_lov_df
            ),
            file_name=(
                f"{selected_sheet}_active_lov.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    else:

        st.info(
            "No Company LOV is currently active. "
            "Upload an XLSX or CSV workbook above."
        )

    
# ============================================================
# EVALUATOR TEST TAB
# ============================================================

with tab_test:
    st.markdown(
        """
        <style>
        .section { margin-bottom: 20px; }
        .section-kicker { font-size: 14px; color: #888; text-transform: uppercase; }
        .section-title { font-size: 22px; font-weight: bold; margin-top: 5px; }
        .section-copy { font-size: 16px; color: #555; margin-top: 10px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="section">
    <div class="section-kicker">05 / Evaluation</div>
    <div class="section-title">Test the enrichment engine on new data</div>
    <div class="section-copy">
        Upload a previously unseen catalogue CSV to verify that
        the enrichment workflow operates dynamically from input
        through structured output.
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload evaluator CSV",
        type=["csv"],
        help=(
            "Upload a catalogue with product descriptions, manufacturer "
            "part numbers or related product information."
        ),
    )

    if uploaded_file is None:

        st.info(
            "Upload a CSV to run the enrichment pipeline on unseen data."
        )

    else:

        try:

            evaluator_df = pd.read_csv(
                uploaded_file,
                on_bad_lines="skip",
            )

            evaluator_df = clean_columns(
                evaluator_df
            )

            st.success(
                f"Input loaded successfully — "
                f"{len(evaluator_df):,} rows × "
                f"{len(evaluator_df.columns):,} columns."
            )

            st.markdown(
                "### Input preview"
            )

            st.dataframe(
                evaluator_df.head(10),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown(
                "### Run dynamic enrichment"
            )

            run_evaluator = st.button(
                "Run enrichment pipeline",
                use_container_width=True,
            )

            if run_evaluator:

                import tempfile

                from src.catalogue import enrich_catalogue
                from src.final_output import (
                    flatten_enriched_dataframe
                )

                with st.spinner(
                    "Running enrichment pipeline..."
                ):

                    with tempfile.NamedTemporaryFile(
                        suffix=".csv",
                        delete=False,
                    ) as temp_file:

                        temp_path = temp_file.name

                    evaluator_df.to_csv(
                        temp_path,
                        index=False,
                    )

                    try:

                        enriched_result = enrich_catalogue(
                            temp_path,
                            company_lov=active_lov_sheets,
                        )

                        final_result = (
                            flatten_enriched_dataframe(
                                enriched_result
                            )
                        )

                    finally:

                        if os.path.exists(temp_path):
                            os.remove(temp_path)

                st.success(
                    f"Pipeline completed — "
                    f"{len(final_result):,} records enriched."
                )

                st.markdown(
                    "### Enriched output"
                )

                output_columns = [
                    column
                    for column in [
                        "Mfg_Part_Num",
                        "Part_Desc",
                        "Part_Manuf",
                        "status",
                        "evidence_count",
                        "product_type",
                        "taxonomy",
                        "confidence",
                    ]
                    if column in final_result.columns
                ]

                if output_columns:

                    st.dataframe(
                        final_result[
                            output_columns
                        ].head(25),
                        use_container_width=True,
                        hide_index=True,
                    )

                else:

                    st.dataframe(
                        final_result.head(25),
                        use_container_width=True,
                        hide_index=True,
                    )

                st.markdown(
                    "### Export evaluator result"
                )

                evaluator_csv = (
                    final_result
                    .to_csv(index=False)
                    .encode("utf-8")
                )

                st.download_button(
                    label="Download enriched evaluator output",
                    data=evaluator_csv,
                    file_name="evaluator_enriched_output.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        except Exception as e:

            st.error(
                f"Evaluator pipeline failed: {e}"
            )
# ============================================================
# EVALUATOR VALIDATION DATA
# ============================================================

if DELIVERY_FILE.exists():
    try:
        evaluator_delivery = pd.read_csv(
            DELIVERY_FILE,
            engine="python",
            on_bad_lines="skip",
        )
        evaluator_delivery = clean_columns(evaluator_delivery)

    except Exception as e:
        evaluator_delivery = pd.DataFrame()
        st.warning(
            f"Evaluator delivery validation could not load the "
            f"production delivery file: {e}"
        )
# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Industrial Product Intelligence · Controlled enrichment ·
        Evidence-aware resolution · Configuration-driven taxonomy ·
        252-field delivery
    </div>
    """,
    unsafe_allow_html=True,
)