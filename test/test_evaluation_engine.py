import pandas as pd

from src.evaluation_engine import (
    evaluate,
)


def test_evaluation_accuracy():

    expected = pd.DataFrame({
        "brand": [
            "3M",
            "Diablo",
        ],
        "manufacturer": [
            "3M Company",
            "Freud Inc",
        ],
    })

    actual = pd.DataFrame({
        "brand": [
            "3M",
            "Wrong",
        ],
        "manufacturer": [
            "3M Company",
            "Freud Inc",
        ],
    })

    result = evaluate(
        expected,
        actual,
        [
            "brand",
            "manufacturer",
        ],
    )

    assert result.accuracy == 0.75


def test_evaluation_coverage():

    expected = pd.DataFrame({
        "brand": [
            "3M",
            "Diablo",
        ],
    })

    actual = pd.DataFrame({
        "brand": [
            "3M",
            "",
        ],
    })

    result = evaluate(
        expected,
        actual,
        ["brand"],
    )

    assert (
        result.coverage_metrics["brand"]
        == 0.5
    )