from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class EvaluationResult:

    total_rows: int
    evaluated_fields: int
    correct_fields: int
    accuracy: float
    field_metrics: dict
    coverage_metrics: dict


def _normalize(value: Any) -> str:

    if value is None:
        return ""

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def field_accuracy(
    expected: pd.Series,
    actual: pd.Series,
) -> float:

    total = 0
    correct = 0

    for exp, act in zip(
        expected,
        actual,
    ):

        exp_norm = _normalize(exp)

        act_norm = _normalize(act)

        if not exp_norm:
            continue

        total += 1

        if exp_norm == act_norm:
            correct += 1

    if total == 0:
        return 0.0

    return correct / total


def field_coverage(
    series: pd.Series,
) -> float:

    if len(series) == 0:
        return 0.0

    populated = sum(
        1
        for value in series
        if _normalize(value)
    )

    return populated / len(series)


def evaluate(
    expected: pd.DataFrame,
    actual: pd.DataFrame,
    fields: list[str],
) -> EvaluationResult:

    field_metrics = {}

    total_evaluated = 0
    total_correct = 0

    coverage_metrics = {}

    for field in fields:

        if (
            field not in expected.columns
            or field not in actual.columns
        ):
            continue

        expected_series = expected[field]

        actual_series = actual[field]

        accuracy = field_accuracy(
            expected_series,
            actual_series,
        )

        coverage = field_coverage(
            actual_series
        )

        field_metrics[field] = accuracy

        coverage_metrics[field] = coverage

        for exp, act in zip(
            expected_series,
            actual_series,
        ):

            exp_norm = _normalize(exp)

            if not exp_norm:
                continue

            total_evaluated += 1

            if (
                exp_norm
                == _normalize(act)
            ):

                total_correct += 1

    overall = (
        total_correct / total_evaluated
        if total_evaluated
        else 0.0
    )

    return EvaluationResult(
        total_rows=len(expected),
        evaluated_fields=total_evaluated,
        correct_fields=total_correct,
        accuracy=overall,
        field_metrics=field_metrics,
        coverage_metrics=coverage_metrics,
    )


def print_report(
    result: EvaluationResult,
):

    print(
    "\nINTERPRETATION"
)

    if result.accuracy >= 0.90:
     print("Strong field-level agreement.")

    elif result.accuracy >= 0.75:

     print("Good agreement with room for improvement.")

    else:

     print("Significant enrichment gaps remain.")
     
def no_invention_rate(
    expected: pd.DataFrame,
    actual: pd.DataFrame,
    fields: list[str],
) -> float:

    total = 0
    safe = 0

    for field in fields:

        if (
            field not in expected.columns
            or field not in actual.columns
        ):
            continue

        expected_values = {
            _normalize(value)
            for value in expected[field]
            if _normalize(value)
        }

        for value in actual[field]:

            normalized = _normalize(value)

            if not normalized:
                continue

            total += 1

            if normalized in expected_values:
                safe += 1

    if total == 0:
        return 0.0

    return safe / total