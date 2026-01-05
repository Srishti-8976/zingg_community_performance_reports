import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Path where performance repo is checked out
CSV_DIR = Path("zingg_performance/results")
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

csv_files = list(CSV_DIR.glob("*.csv"))
if not csv_files:
    raise RuntimeError("No CSV files found in zingg_performance/results")

dates = []
durations = []

for csv_file in sorted(csv_files):
    df = pd.read_csv(csv_file)

    # REQUIRED columns from perf_csv_writer
    required_cols = {"date", "time", "test"}
    if not required_cols.issubset(df.columns):
        raise RuntimeError(
            f"CSV format mismatch in {csv_file.name}. Found columns: {list(df.columns)}"
        )

    # Use first numeric column as runtime metric
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        raise RuntimeError(f"No numeric columns found in {csv_file.name}")

    metric_col = numeric_cols[0]

    dates.append(df["date"].iloc[0])
    durations.append(df[metric_col].iloc[0])

# Plot
plt.figure(figsize=(8, 4))
plt.plot(dates, durations, marker="o")
plt.xlabel("Date")
plt.ylabel("Runtime")
plt.title("Zingg FEBRL Performance Trend")
plt.xticks(rotation=45)
plt.tight_layout()

output_path = PLOTS_DIR / "febrl_runtime.png"
plt.savefig(output_path)
plt.close()

print("Plot saved to:", output_path)
