import pandas as pd

from src.identity import build_identity


def test_identity_extraction():

    row = pd.Series({
        "Mfg_Part_Num": "49-94-0107",
        "Part_Desc": (
            '49-94-0107 Milw 4-1/2"x.045"x7/8" '
            "Performance+ Metal Cut Off Disc"
        ),
        "E1_Brand": "-- Unbranded --",
        "Unilog_Brand": "-- No Unilog Brand --",
        "DIB_Brand": "-- No DIB Brand --",
        "Part_Manuf": "Milwaukee Accessory (4031)",
    })

    result = build_identity(row)

    assert result["mpn"] == "49-94-0107"
    assert result["manufacturer_candidate"] == "Milwaukee Accessory"
    assert result["brand_candidate"] is None

    assert "49-94-0107" in result["identity_query"]
    assert "Milwaukee Accessory" in result["identity_query"]