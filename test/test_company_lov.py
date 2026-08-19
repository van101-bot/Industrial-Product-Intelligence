from src.company_lov import CompanyLOV


def get_lov():

    return CompanyLOV(
        "data/demo/company_lov_v2.csv"
    )


def test_lov_loads():

    lov = get_lov()

    assert len(lov.attributes()) > 0


def test_exact_value():

    result = get_lov().resolve(
        "Material",
        "Steel",
    )

    assert result["value"] == "Steel"
    assert result["source"] == "company_lov"


def test_alias_resolution():

    result = get_lov().resolve(
        "Material",
        "SS",
    )

    assert result["value"] == "Stainless Steel"


def test_unknown_value_not_invented():

    result = get_lov().resolve(
        "Material",
        "Unobtainium",
    )

    assert result["value"] is None