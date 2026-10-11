from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "dataset" / "cleaned_facilities.csv"


def main():
    if not DATA_FILE.exists():
        print("Cleaned dataset not found.")
        print("Run data-cleaning/clean_data.py first.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("The cleaned dataset has no records.")
        return

    print("\n===== FACILITY DATA ANALYSIS =====")

    print("\n1. Dataset shape")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\n2. First five records")
    print(df.head().to_string(index=False))

    print("\n3. Data types")
    print(df.dtypes)

    print("\n4. Summary statistics")
    print(df.describe(numeric_only=True).round(2))

    print("\n5. Average scores and counts")
    for column in [
        "cleanliness_score", "odor_score",
        "waste_level", "footfall", "complaints"
    ]:
        if column in df.columns:
            print(f"{column}:")
            print(df[column].value_counts().to_string()
                  if column == "waste_level"
                  else df[column].mean())

    print("\n6. Average cleanliness by location")
    print(
        df.groupby("location")["cleanliness_score"]
        .mean().round(2).sort_values(ascending=False)
    )

    print("\n7. Average odor score by location")
    print(
        df.groupby("location")["odor_score"]
        .mean().round(2)
    )

    print("\n8. Total complaints by location")
    print(
        df.groupby("location")["complaints"]
        .sum().sort_values(ascending=False)
    )

    print("\n9. Total footfall by location")
    print(
        df.groupby("location")["footfall"]
        .sum().sort_values(ascending=False)
    )

    print("\n10. Facilities with the most complaints")
    print(
        df.sort_values("complaints", ascending=False)[
            ["facility_id", "location", "complaints"]
        ].head(5).to_string(index=False)
    )

    print("\n11. Facilities with lowest cleanliness")
    print(
        df.sort_values("cleanliness_score")[
            ["facility_id", "location", "cleanliness_score"]
        ].head(5).to_string(index=False)
    )

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()