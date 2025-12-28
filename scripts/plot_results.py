import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "perf_test"
PLOTS_DIR = "plots"

os.makedirs(PLOTS_DIR, exist_ok=True)

csv_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".csv")]

for csv in csv_files:
    df = pd.read_csv(os.path.join(RESULTS_DIR, csv))

    name = csv.replace(".csv", "")

    # ---- Performance Metrics ----
    plt.figure()
    if "precision" in df.columns:
        plt.plot(df["precision"], label="Precision")
    if "recall" in df.columns:
        plt.plot(df["recall"], label="Recall")
    if "f1" in df.columns:
        plt.plot(df["f1"], label="F1")

    plt.legend()
    plt.title(f"Performance Metrics – {name}")
    plt.xlabel("Test Index")
    plt.ylabel("Score")
    plt.savefig(f"{PLOTS_DIR}/{name}_metrics.png")
    plt.close()

    # ---- Runtime ----
    if "runtime" in df.columns:
        plt.figure()
        plt.bar(range(len(df)), df["runtime"])
        plt.title(f"Runtime – {name}")
        plt.xlabel("Test Index")
        plt.ylabel("Time (seconds)")
        plt.savefig(f"{PLOTS_DIR}/{name}_runtime.png")
        plt.close()
    
# trigger workflow

