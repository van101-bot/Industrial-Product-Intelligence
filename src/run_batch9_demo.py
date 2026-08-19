from src.company_lov import CompanyLOV


def main():

    print("=" * 70)
    print("BATCH 9 — CONFIGURATION-DRIVEN INTELLIGENCE")
    print("=" * 70)

    lov = CompanyLOV(
        "data/demo/company_lov_v2.csv"
    )

    print()
    print("ATTRIBUTES:")
    print(lov.attributes())

    print()
    print("CONTROLLED MATERIAL VALUES:")
    print(lov.values("Material"))

    print()
    print("RESOLUTION TESTS:")

    tests = [
        ("Material", "steel"),
        ("Material", "SS"),
        ("Material", "stainless steel"),
        ("Material", "titanium"),
        ("Material", "something unknown"),
    ]

    for attribute, value in tests:

        result = lov.resolve(
            attribute,
            value,
        )

        print()
        print(
            f"{attribute} = {value}"
        )
        print(result)

    print()
    print("=" * 70)
    print("BATCH 9 DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()