import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

CSV_DIR = Path("zingg_performance_repo/results")
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Load CSV files
# --------------------------------------------------

csv_files = sorted(CSV_DIR.glob("*.csv"))

if not csv_files:
    raise RuntimeError("No CSV files found in zingg_performance_repo/results")

print(f"[INFO] Found {len(csv_files)} CSV files")

dfs = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    # Validate required columns
    for col in ["date", "train", "match"]:
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in {csv_file.name}")

    df["date"] = pd.to_datetime(df["date"])
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True).sort_values("date")

# --------------------------------------------------
# Plot: TRAIN vs DATE
# --------------------------------------------------

plt.figure(figsize=(8, 5))
plt.plot(data["date"], data["train"], marker="o")
plt.xlabel("Date")
plt.ylabel("Train Time")
plt.title("Train vs Date")
plt.grid(True)
plt.tight_layout()

train_plot_path = PLOTS_DIR / "train_vs_date.png"
plt.savefig(train_plot_path, dpi=150)
plt.close()

print(f"[INFO] Updated plot: {train_plot_path}")

# --------------------------------------------------
# Plot: MATCH vs DATE
# --------------------------------------------------

plt.figure(figsize=(8, 5))
plt.plot(data["date"], data["match"], marker="o")
plt.xlabel("Date")
plt.ylabel("Match Time")
plt.title("Match vs Date")
plt.grid(True)
plt.tight_layout()

match_plot_path = PLOTS_DIR / "match_vs_date.png"
plt.savefig(match_plot_path, dpi=150)
plt.close()

print(f"[INFO] Updated plot: {match_plot_path}")

print("✅ Performance plots generated successfully")
