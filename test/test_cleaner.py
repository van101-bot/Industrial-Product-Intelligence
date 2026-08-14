import pandas as pd

from src.cleaner import clean_product_row


def test_placeholder_brands_are_removed():

    row = pd.Series({
        "Mfg_Part_Num": "TEST123",
        "Part_Desc": "Test Product",
        "E1_Brand": "-- Unbranded --",
        "Unilog_Brand": "-- No Unilog Brand --",
        "DIB_Brand": "-- No DIB Brand --",
        "Part_Manuf": "Test Manufacturer",
    })

    result = clean_product_row(row)

    assert result["mpn"] == "TEST123"
    assert result["part_description"] == "Test Product"

    assert result["e1_brand"] is None
    assert result["unilog_brand"] is None
    assert result["dib_brand"] is None

    assert result["manufacturer"] == "Test Manufacturer"