from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "dataset" / "cleaned_facilities.csv"
OUTPUT_DIR = BASE_DIR / "visualizations"


def main():
    if not DATA_FILE.exists():
        print("Cleaned dataset not found.")
        print("Run data-cleaning/clean_data.py first.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("No data available for plotting.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Bar chart: average cleanliness by location
    average_cleanliness = (
        df.groupby("location")["cleanliness_score"].mean()
    )

    average_cleanliness.plot(kind="bar")
    plt.title("Average Cleanliness Score by Location")
    plt.xlabel("Location")
    plt.ylabel("Average Cleanliness Score")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "cleanliness_by_location.png")
    plt.close()

    # 2. Line chart: complaints by inspection date
    df["inspection_date"] = pd.to_datetime(
        df["inspection_date"], errors="coerce"
    )

    daily = (
        df.groupby("inspection_date")["complaints"]
        .sum().sort_index()
    )

    daily.plot(kind="line", marker="o")
    plt.title("Complaints Over Inspection Dates")
    plt.xlabel("Inspection Date")
    plt.ylabel("Total Complaints")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "complaints_over_time.png")
    plt.close()

    # 3. Histogram: distribution of footfall
    df["footfall"].plot(kind="hist", bins=8)
    plt.title("Distribution of Facility Footfall")
    plt.xlabel("Footfall")
    plt.ylabel("Number of Facilities")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "footfall_histogram.png")
    plt.close()

    # 4. Scatter plot: footfall versus complaints
    plt.scatter(df["footfall"], df["complaints"])
    plt.title("Footfall vs Complaints")
    plt.xlabel("Footfall")
    plt.ylabel("Complaints")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "footfall_vs_complaints.png")
    plt.close()

    print("All charts have been saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()