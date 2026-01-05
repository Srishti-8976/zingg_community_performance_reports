import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths
PERF_REPO_RESULTS = "../zingg_performance/results"
PLOTS_DIR = "plots"

os.makedirs(PLOTS_DIR, exist_ok=True)

# Collect all CSV files
csv_files = []
for root, _, files in os.walk(PERF_REPO_RESULTS):
    for f in files:
        if f.endswith(".csv"):
            csv_files.append(os.path.join(root, f))

if not csv_files:
    raise RuntimeError("No CSV files found in zingg_performance/results")

# Load and combine CSVs
dfs = []
for csv in csv_files:
    try:
        df = pd.read_csv(csv)
        dfs.append(df)
    except Exception as e:
        print(f"Skipping {csv}: {e}")

data = pd.concat(dfs, ignore_index=True)

# Convert date + time to datetime
data["datetime"] = pd.to_datetime(
    data["date"] + " " + data["time"],
    errors="coerce"
)

data = data.sort_values("datetime")

# Pick numeric columns (performance phases)
numeric_cols = data.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    raise RuntimeError("No numeric columns found for plotting")

# -------- Plot 1: Total runtime trend (sum of phases) --------
data["total_runtime"] = data[numeric_cols].sum(axis=1)

plt.figure()
plt.plot(data["datetime"], data["total_runtime"])
plt.xlabel("Run Time")
plt.ylabel("Total Runtime")
plt.title("FEBRL Performance Trend")
plt.xticks(rotation=45)
plt.tight_layout()

runtime_plot_path = os.path.join(PLOTS_DIR, "febrl_runtime_trend.png")
plt.savefig(runtime_plot_path)
plt.close()

print(f"Saved plot: {runtime_plot_path}")

