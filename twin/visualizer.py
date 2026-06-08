import matplotlib.pyplot as plt
import os
from config import FEATURES, RESULTS_DIR

os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_sensor_streams(df):
    fig, axes = plt.subplots(len(FEATURES), 1, figsize=(14, 20), sharex=True)
    for i, col in enumerate(FEATURES):
        axes[i].plot(df["datetime"], df[col], linewidth=0.8, color="steelblue")
        mask = df["anomaly"] == 1
        axes[i].scatter(df["datetime"][mask], df[col][mask],
                        color="red", s=12, zorder=5, label="Anomaly")
        axes[i].set_ylabel(col, fontsize=8)
        axes[i].grid(True, alpha=0.3)
    axes[0].legend(loc="upper right")
    plt.suptitle("SKAB — All Sensor Streams with Ground Truth Anomalies",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    path = f"{RESULTS_DIR}/sensor_streams.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Visualizer] Saved {path}")

def plot_anomaly_scores(df, scores):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    ax1.plot(df["datetime"], df["Pressure"], color="steelblue", linewidth=0.8)
    mask = df["anomaly"] == 1
    ax1.scatter(df["datetime"][mask], df["Pressure"][mask],
                color="red", s=12, zorder=5, label="True Anomaly")
    ax1.set_ylabel("Pressure")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax2.plot(df["datetime"], scores, color="darkorange", linewidth=0.8, label="IF Score")
    ax2.axhline(0, color="red", linestyle="--", linewidth=1, label="Threshold")
    pred_mask = df["predicted_anomaly"] == 1
    ax2.scatter(df["datetime"][pred_mask], scores[pred_mask],
                color="red", s=15, zorder=5, label="Detected")
    ax2.set_ylabel("Anomaly Score")
    ax2.set_xlabel("Time")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.suptitle("Isolation Forest — Anomaly Detection Results",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    path = f"{RESULTS_DIR}/anomaly_scores.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Visualizer] Saved {path}")

def plot_comparison(metrics_baseline, metrics_upgraded):
    labels = ["Precision", "Recall", "F1-Score"]
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(10, 7))
    bars1 = ax.bar([i - 0.2 for i in x], metrics_baseline, 0.35,
                   label="Baseline (raw features)", color="steelblue", alpha=0.85)
    bars2 = ax.bar([i + 0.2 for i in x], metrics_upgraded, 0.35,
                   label="Rolling Window Features", color="mediumpurple", alpha=0.85)
    for bar in list(bars1) + list(bars2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{bar.get_height():.2f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Score", fontsize=12)
    p_up = metrics_upgraded[0]
    r_up = metrics_upgraded[1]
    f_up = metrics_upgraded[2]
    ax.set_title(
        f"Baseline vs Rolling Window Feature Engineering\n"
        f"Rolling Window: Precision {p_up:.2f} | Recall {r_up:.2f} | F1 {f_up:.2f}",
        fontweight="bold", fontsize=12)
    ax.legend(fontsize=11, loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")
    fig.text(0.5, 0.01,
             "Safety-critical insight: In industrial monitoring, high recall = fewer missed faults",
             ha="center", fontsize=10, color="purple", style="italic")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    path = f"{RESULTS_DIR}/model_comparison.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Visualizer] Saved {path}")
