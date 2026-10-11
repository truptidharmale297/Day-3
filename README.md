Day 3 — Data Analysis and Python for AI/ML

1. Project Overview

This project focuses on inspecting, cleaning, analyzing, and visualizing facility inspection data using Python.

The dataset includes facility location, cleanliness score, odor score, waste level, water availability, footfall, complaints, and inspection date.

2. Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- CSV
- Visual Studio Code

3. Project Structure

- "dataset/" — Original and cleaned facility datasets and data quality report.
- "data-cleaning/" — Script for identifying and handling data-quality issues.
- "analysis/" — Script for statistical analysis and comparisons.
- "visualizations/" — Script and generated charts.
- "README.md" — Project documentation.

4. Features

- Inspect dataset dimensions and data types.
- Identify missing values and duplicate rows.
- Validate scores, categories, counts, and inspection dates.
- Detect possible outliers using the IQR method.
- Handle missing and invalid values.
- Generate a cleaned dataset.
- Calculate summary statistics and group-wise averages.
- Compare complaints, footfall, and cleanliness across locations.
- Generate bar charts, line charts, histograms, and scatter plots.

5. Setup Instructions

1. Install Python 3.
2. Install Visual Studio Code.
3. Open the "day-03" folder in VS Code.
4. Open Terminal and install the required libraries:

python -m pip install numpy pandas matplotlib

6. How to Run the Project

Run the commands from the "day-03" root folder in this order.

Step 1: Clean the dataset

python data-cleaning/clean_data.py

Step 2: Analyze the cleaned data

python analysis/analyze_data.py

Step 3: Generate visualizations

python visualizations/create_charts.py

7. Data Cleaning

The cleaning script removes exact duplicate rows, converts invalid numeric values to missing values, validates score ranges, standardizes categories, and identifies possible outliers.

Missing numeric values are filled using the median, missing categories using the mode, and records without a valid facility ID or inspection date are removed.

Possible outliers are reported for review rather than automatically deleted.

8. Visualizations

The project generates:

- Average cleanliness by location.
- Complaints over inspection dates.
- Distribution of facility footfall.
- Relationship between footfall and complaints.

9. Findings

The sample dataset is designed to demonstrate duplicate detection, missing values, invalid scores, invalid dates, and possible outliers.

Actual findings are available in the generated data quality report, analysis output, and chart files.

10. Conclusion

This project demonstrates data cleaning, data transformation, statistical analysis, and visualization using Python libraries. These skills are useful for preparing data for further AI and machine learning tasks.
