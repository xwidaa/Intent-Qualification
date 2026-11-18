from pathlib import Path
import pandas as pd


DATA_PATH = Path("data/companies.jsonl")


def load_data(path):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_json(path, lines=True)
    return df


def analyze_dataset(df):
    print("\n=== DATASET OVERVIEW ===")
    print(f"Total companies: {len(df)}")
    print(f"Total fields: {len(df.columns)}")

    print("\n=== AVAILABLE FIELDS ===")
    for column in df.columns:
        print(column)

    print("\n=== MISSING VALUES ===")

    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": (
            df.isna().mean() * 100
        ).round(2)
    })

    print(missing.sort_values(
        "missing_percent", ascending=False
    ).to_string())

    print("\n=== NUMERICAL STATISTICS ===")

    numeric_columns = [
        "employee_count",
        "revenue",
        "year_founded"
    ]

    available_numeric = [
        col for col in numeric_columns
        if col in df.columns
    ]

    if available_numeric:
        numeric_df = df[available_numeric].apply(
            pd.to_numeric, errors="coerce"
        )
        print(numeric_df.describe().to_string())

    print("\n=== TOP INDUSTRIES ===")

    if "primary_naics" in df.columns:
        industries = df["primary_naics"].apply(
            lambda x: x.get("label", "Unknown")
            if isinstance(x, dict)
            else str(x) if pd.notna(x) else "Unknown"
        )

        print(industries.value_counts().head(15).to_string())

    print("\n=== SAMPLE COMPANIES ===")

    columns = [
        "operational_name",
        "address",
        "description",
        "core_offerings"
    ]

    available = [
        col for col in columns
        if col in df.columns
    ]

    for index, row in df[available].head(3).iterrows():
        print(f"\nCompany {index + 1}")
        for col in available:
            print(f"{col}: {row[col]}")

    print("\n=== DUPLICATE WEBSITES ===")

    if "website" in df.columns:
        websites = df["website"].dropna()
        print(f"Duplicate websites: {websites.duplicated().sum()}")


def main():
    df = load_data(DATA_PATH)
    analyze_dataset(df)


if __name__ == "__main__":
    main()
