from src.cleaner import clean_product_row
from src.identity import build_identity


def test_real_dcb518_product_identity():

    row = {
        "Mfg_Part_Num": "DCB518ASTS06G",
        "Part_Desc": 'DCB518ASTS06G Diablo 1/2"x18" - Sanding Belt 6pc',
        "E1_Brand": "-- Unbranded --",
        "Unilog_Brand": "-- No Unilog Brand --",
        "DIB_Brand": "-- No DIB Brand --",
        "Part_Manuf": "Freud Inc (2435)",
    }

    cleaned = clean_product_row(row)

    identity = build_identity(cleaned)

    print("\n=== REAL PRODUCT IDENTITY ===")
    print(identity)

    assert identity is not None