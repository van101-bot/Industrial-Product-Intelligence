import pandas as pd

from src.catalogue import enrich_catalogue


def test_catalogue_processor_returns_one_result_per_row(
    tmp_path,
    monkeypatch,
):

    input_file = tmp_path / "input.csv"

    df = pd.DataFrame([
        {
            "Mfg_Part_Num": "TEST-001",
            "Part_Desc": '4-1/2"x.045"x7/8" Metal Cut Off Disc',
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
            "Part_Manuf": "Test Manufacturer (001)",
        },
        {
            "Mfg_Part_Num": "TEST-002",
            "Part_Desc": "Generic Sanding Belt",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
            "Part_Manuf": "Test Manufacturer (002)",
        },
    ])

    df.to_csv(input_file, index=False)

    def fake_enrich_product(row):

        return {
            "status": "accepted",
            "identity": {
                "mpn": row["Mfg_Part_Num"]
            },
            "brand": {},
            "manufacturer": {},
            "attributes": {},
            "evidence": [],
        }

    monkeypatch.setattr(
        "src.catalogue.enrich_product",
        fake_enrich_product,
    )

    result = enrich_catalogue(str(input_file))

    assert len(result) == 2
    assert list(result["Mfg_Part_Num"]) == [
        "TEST-001",
        "TEST-002",
    ]