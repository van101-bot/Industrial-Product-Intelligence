from time import perf_counter


def benchmark(function, *args, **kwargs):

    start = perf_counter()

    result = function(
        *args,
        **kwargs
    )

    elapsed = perf_counter() - start

    rows = len(result) if hasattr(result, "__len__") else 1

    return {
        "elapsed_seconds": round(elapsed, 3),
        "rows_processed": rows,
        "rows_per_second": round(
            rows / elapsed,
            2
        ) if elapsed > 0 else None,
        "result": result,
    }