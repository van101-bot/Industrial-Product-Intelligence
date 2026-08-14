from data_loader import load_input_data


def main():
    df = load_input_data()

    print("=== DATASET PROFILE ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\n=== UNIQUE VALUES ===")

    for column in df.columns:
        print(f"\n{column}")
        print(f"Unique: {df[column].nunique(dropna=False)}")
        print(df[column].value_counts(dropna=False).head(10))


if __name__ == "__main__":
    main()