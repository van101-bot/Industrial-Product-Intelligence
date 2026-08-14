from src.brand_resolver import resolve_brand


def test_resolve_diablo_from_real_product():

    row = {
        "mpn": "DCB518ASTS06G",
        "part_description":
            'DCB518ASTS06G Diablo 1/2"x18" - Sanding Belt 6pc',
        "e1_brand": None,
        "unilog_brand": None,
        "dib_brand": None,
        "manufacturer": "Freud Inc (2435)",
    }

    result = resolve_brand(row)

    print("\n=== BRAND RESOLUTION ===")
    print(result)

    assert result["brand"] == "Diablo"
    assert result["source"] == "description"
    assert result["confidence"] > 0