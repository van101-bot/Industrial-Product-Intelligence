from src.master_data import (
    load_manufacturer_brand_master,
    manufacturer_names,
    brand_names,
)


def test_manufacturer_brand_master():

    df = load_manufacturer_brand_master()

    print("\n=== MASTER DATA ===")
    print("Rows:", len(df))
    print("Manufacturers:", len(manufacturer_names()))
    print("Brands:", len(brand_names()))

    assert len(df) > 0
    assert "MANUFACTURER_NAME" in df.columns
    assert "MANUFACTURER_CODE" in df.columns
    assert "BRAND_NAME" in df.columns
    assert "BRAND_CODE" in df.columns


def test_master_has_manufacturers():

    names = manufacturer_names()

    assert len(names) >= 50


def test_master_has_brands():

    names = brand_names()

    assert len(names) >= 20