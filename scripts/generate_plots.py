from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_DIR = Path("zingg_performance_repo/results")

csv_files = list(CSV_DIR.glob("*.csv"))

if not csv_files:
    raise RuntimeError(f"No CSV files found in {CSV_DIR.resolve()}")

print(f"Found {len(csv_files)} CSV files")

# Example: plot duration vs timestamp
durations = []
labels = []

for csv_file in sorted(csv_files):
    df = pd.read_csv(csv_file)
    durations.append(float(df["duration_sec"].iloc[0]))
    labels.append(csv_file.stem)

plt.figure()
plt.plot(labels, durations, marker="o")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Duration (seconds)")
plt.title("FEBRL Performance Over Time")
plt.tight_layout()

OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

plot_path = OUTPUT_DIR / "febrl_performance.png"
plt.savefig(plot_path)
plt.close()

print("Plot saved to", plot_path)


