import pandas as pd

from src.lov_adapter import LOVAdapter


def test_lov_adapter_loads_csv(tmp_path):

    path = tmp_path / "lov.csv"

    pd.DataFrame({
        "Classpath": [
            "Abrasives > Cut-Off Discs",
            "Abrasives > Grinding Wheels",
        ],
        "Attribute Label": [
            "Diameter",
            "Thickness",
        ],
    }).to_csv(path, index=False)

    adapter = LOVAdapter(path)

    assert len(adapter.taxonomy_values()) == 2
    assert len(adapter.attribute_values()) == 2


def test_lov_adapter_ignores_placeholders(tmp_path):

    path = tmp_path / "lov.csv"

    pd.DataFrame({
        "Category": [
            "Abrasives",
            "--",
            None,
            "",
        ]
    }).to_csv(path, index=False)

    adapter = LOVAdapter(path)

    assert adapter.taxonomy_values() == [
        "Abrasives"
    ]


def test_lov_adapter_summary(tmp_path):

    path = tmp_path / "lov.csv"

    pd.DataFrame({
        "Taxonomy": ["Abrasives"],
        "Attribute": ["Diameter"],
    }).to_csv(path, index=False)

    adapter = LOVAdapter(path)

    summary = adapter.summary()

    assert summary["taxonomy_values"] == 1
    assert summary["attribute_values"] == 1

