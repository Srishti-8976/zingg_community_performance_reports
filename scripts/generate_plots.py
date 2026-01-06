import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

PERF_REPO = Path("zingg_performance_repo/results")
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

csv_files = sorted(PERF_REPO.glob("*.csv"))

if not csv_files:
    raise RuntimeError("No CSV files found in zingg_performance_repo/results")

print(f"Found {len(csv_files)} CSV files")

# --------------------------------------------------
# Load & merge CSVs
# --------------------------------------------------

dfs = []
for csv in csv_files:
    df = pd.read_csv(csv)
    df["date"] = pd.to_datetime(df["date"])
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)
data = data.sort_values("date")

# --------------------------------------------------
# Detect numeric metric columns (excluding date)
# --------------------------------------------------

numeric_cols = data.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    raise RuntimeError("No numeric columns found to plot")

print("Numeric metrics found:", numeric_cols)

# --------------------------------------------------
# Plot EACH metric vs date
# --------------------------------------------------

for metric in numeric_cols:
    plt.figure(figsize=(8, 5))
    plt.plot(data["date"], data[metric], marker="o")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.title(f"{metric} vs Date")
    plt.grid(True)

    plot_path = PLOTS_DIR / f"{metric}_vs_date.png"
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

    print(f"Saved plot: {plot_path}")
