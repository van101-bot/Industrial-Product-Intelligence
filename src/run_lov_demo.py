from pathlib import Path
import pandas as pd

from src.lov_profile import load_lov_profile
from src.lov_engine import LOVEngine


def main():

    print("=" * 70)
    print("CONFIGURABLE LOV ENGINE DEMO")
    print("=" * 70)

    lov_files = list(
        Path("data").rglob("*.xlsx")
    )

    if not lov_files:

        print("No XLSX LOV/reference file found.")
        print(
            "The engine can also be tested using a CSV."
        )
        return

    print("\nAvailable reference files:")

    for i, path in enumerate(
        lov_files,
        start=1,
    ):

        print(
            f"{i}. {path}"
        )

    # ---------------------------------------------------------
    # IMPORTANT:
    # Do NOT automatically treat arbitrary reference
    # spreadsheets as LOVs.
    # For the competition demo, choose the appropriate
    # workbook explicitly.
    # ---------------------------------------------------------

    print(
        "\nSet LOV_FILE below to the workbook you want to use."
    )


if __name__ == "__main__":
    main()