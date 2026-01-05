from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_DIR = Path("zingg_performance_repo/results")
csv_files = sorted(CSV_DIR.glob("*.csv"))

if not csv_files:
    raise RuntimeError(f"No CSV files found in {CSV_DIR.resolve()}")

print(f"Found {len(csv_files)} CSV files")

labels = []
total_durations = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    # Fixed columns we ignore
    fixed_cols = {"date", "time", "test"}

    # All numeric phase columns
    phase_cols = [c for c in df.columns if c not in fixed_cols]

    if not phase_cols:
        raise RuntimeError(f"No phase columns found in {csv_file.name}")

    total_time = df[phase_cols].iloc[0].sum()

    labels.append(csv_file.stem)
    total_durations.append(total_time)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(labels, total_durations, marker="o")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Total Runtime (seconds)")
plt.title("FEBRL Performance Trend")
plt.tight_layout()

OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

plot_path = OUTPUT_DIR / "febrl_performance.png"
plt.savefig(plot_path)
plt.close()

print("Plot saved to:", plot_path)

print("Plot saved to", plot_path)


