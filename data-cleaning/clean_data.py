from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "dataset" / "facilities.csv"
OUTPUT_FILE = BASE_DIR / "dataset" / "cleaned_facilities.csv"
REPORT_FILE = BASE_DIR / "dataset" / "data_quality_report.txt"


def main():
    if not INPUT_FILE.exists():
        print("Dataset not found:", INPUT_FILE)
        return

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "facility_id", "location", "cleanliness_score",
        "odor_score", "waste_level", "water_availability",
        "footfall", "complaints", "inspection_date"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        return

    report = []
    report.append("FACILITY DATA QUALITY REPORT")
    report.append("=" * 35)
    report.append(f"Original row count: {len(df)}")
    report.append("\nMissing values before cleaning:")
    report.append(df.isnull().sum().to_string())
    report.append(
        f"\nExact duplicate rows: {df.duplicated().sum()}"
    )

    # Remove leading/trailing spaces from text columns
    for column in [
        "facility_id", "location", "waste_level",
        "water_availability"
    ]:
        df[column] = df[column].astype("string").str.strip()

    # Remove exact duplicate rows
    df = df.drop_duplicates().copy()

    # Convert numeric fields; invalid text becomes missing
    numeric_columns = [
        "cleanliness_score", "odor_score",
        "footfall", "complaints"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Scores must be between 0 and 10
    for column in ["cleanliness_score", "odor_score"]:
        invalid = ~df[column].between(0, 10)
        report.append(
            f"\nInvalid values in {column}: {int(invalid.sum())}"
        )
        df.loc[invalid, column] = float("nan")

    # Counts cannot be negative
    for column in ["footfall", "complaints"]:
        invalid = df[column] < 0
        report.append(
            f"Negative values in {column}: {int(invalid.sum())}"
        )
        df.loc[invalid, column] = float("nan")

    # Standardize text categories
    df["location"] = df["location"].str.title()
    df["waste_level"] = df["waste_level"].str.title()
    df["water_availability"] = (
        df["water_availability"].str.title()
    )

    # Replace invalid categories with missing values
    df.loc[
        ~df["waste_level"].isin(["Low", "Medium", "High"]),
        "waste_level"
    ] = pd.NA

    df.loc[
        ~df["water_availability"].isin(["Yes", "No"]),
        "water_availability"
    ] = pd.NA

    # Convert invalid dates to missing dates
    df["inspection_date"] = pd.to_datetime(
        df["inspection_date"], errors="coerce"
    )

    report.append(
        "\nInvalid or missing dates after conversion: "
        + str(df["inspection_date"].isna().sum())
    )

    # Identify possible outliers using IQR
    report.append("\nPOSSIBLE NUMERIC OUTLIERS (IQR)")
    for column in numeric_columns:
        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[column].notna() & (
            (df[column] < lower) | (df[column] > upper)
        )

        report.append(
            f"{column}: {int(outliers.sum())} possible outlier(s)"
        )
        if outliers.any():
            report.append(
                "  Facility IDs: "
                + ", ".join(df.loc[outliers, "facility_id"].astype(str))
            )

    # Fill missing numeric values with the median
    for column in numeric_columns:
        median_value = df[column].median()
        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

    # Fill missing categories with the most common value
    for column in [
        "location", "waste_level", "water_availability"
    ]:
        mode_values = df[column].mode()
        if not mode_values.empty:
            df[column] = df[column].fillna(mode_values.iloc[0])

    # Remove rows with missing essential identifiers or dates
    df = df.dropna(
        subset=["facility_id", "inspection_date"]
    ).copy()

    # Save dates in a readable format
    df["inspection_date"] = (
        df["inspection_date"].dt.strftime("%Y-%m-%d")
    )

    df.to_csv(OUTPUT_FILE, index=False)

    report.append(f"\nFinal cleaned row count: {len(df)}")
    report.append(f"Rows saved to: {OUTPUT_FILE.name}")
    report.append("\nMissing values after cleaning:")
    report.append(df.isnull().sum().to_string())

    REPORT_FILE.write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("\n".join(report))
    print("\nCleaned dataset saved:", OUTPUT_FILE)
    print("Quality report saved:", REPORT_FILE)


if __name__ == "__main__":
    main()