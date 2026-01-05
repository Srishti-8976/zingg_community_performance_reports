from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_DIR = Path("zingg_performance_repo/results")
csv_files = sorted(CSV_DIR.glob("*.csv"))

if not csv_files:
    raise RuntimeError(f"No CSV files found in {CSV_DIR.resolve()}")

print(f"Found {len(csv_files)} CSV files")

labels = []
durations = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    if "duration_sec" not in df.columns:
        raise RuntimeError(
            f"'duration_sec' column not found in {csv_file.name}. "
            f"Found columns: {list(df.columns)}"
        )

    durations.append(float(df["duration_sec"].iloc[0]))
    labels.append(csv_file.stem)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(labels, durations, marker="o")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Runtime (seconds)")
plt.title("FEBRL Performance Trend")
plt.tight_layout()

OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

plot_path = OUTPUT_DIR / "febrl_performance.png"
plt.savefig(plot_path)
plt.close()

print("Plot saved to:", plot_path)
