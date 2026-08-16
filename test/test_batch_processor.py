import pandas as pd

from src.batch_processor import process_dataframe


def test_batch_processor_returns_one_result_per_row():

    df = pd.DataFrame([
        {
            "Mfg_Part_Num": "TEST-001",
            "Part_Desc": "Generic Metal Cut Off Disc",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
            "Part_Manuf": "Test Manufacturer",
        }
    ])

    result = process_dataframe(df)

    assert len(result) == 1
    assert "Mfg_Part_Num" in result.columns
    assert "Status" in result.columns