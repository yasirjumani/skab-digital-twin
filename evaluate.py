import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from twin.ingestion import load_data
from twin.features import add_rolling_features, get_feature_columns
from twin.visualizer import plot_sensor_streams, plot_anomaly_scores, plot_comparison
from config import FEATURES, TARGET, CALIBRATION_ROWS, RESULTS_DIR
import os

os.makedirs(RESULTS_DIR, exist_ok=True)

def run():
    print("\n=== SKAB Digital Twin — Evaluation Pipeline ===\n")
    df = load_data()

    # Train on first 200 rows, test on remaining
    train = df.iloc[:CALIBRATION_ROWS]
    test  = df.iloc[CALIBRATION_ROWS:].copy()

    # --- Baseline: raw features, no rolling ---
    scaler1 = StandardScaler()
    X_train_base = scaler1.fit_transform(train[FEATURES].fillna(0))
    X_test_base  = scaler1.transform(test[FEATURES].fillna(0))
    model1 = IsolationForest(contamination=0.08, random_state=42)
    model1.fit(X_train_base)
    base_pred = (model1.predict(X_test_base) == -1).astype(int)
    p_b, r_b, f_b, _ = precision_recall_fscore_support(
        test[TARGET].astype(int), base_pred, average="binary", zero_division=0)

    # --- Upgraded: rolling window features ---
    df_feat = add_rolling_features(df)
    feat_cols = get_feature_columns()
    train_feat = df_feat.iloc[:CALIBRATION_ROWS]
    test_feat  = df_feat.iloc[CALIBRATION_ROWS:].copy()

    scaler2 = StandardScaler()
    X_train_roll = scaler2.fit_transform(train_feat[feat_cols].fillna(0))
    X_test_roll  = scaler2.transform(test_feat[feat_cols].fillna(0))
    model2 = IsolationForest(contamination=0.08, n_estimators=150, random_state=42)
    model2.fit(X_train_roll)
    roll_pred = (model2.predict(X_test_roll) == -1).astype(int)
    scores    = model2.decision_function(X_test_roll)
    p_r, r_r, f_r, _ = precision_recall_fscore_support(
        test[TARGET].astype(int), roll_pred, average="binary", zero_division=0)

    test["predicted_anomaly"] = roll_pred

    print("--- Baseline Isolation Forest (raw features, test set) ---")
    print(f"Precision: {p_b:.2f}  Recall: {r_b:.2f}  F1: {f_b:.2f}")
    print("\n--- Upgraded: Rolling Window Features (test set) ---")
    print(f"Precision: {p_r:.2f}  Recall: {r_r:.2f}  F1: {f_r:.2f}")
    print("\n--- Full Report (Rolling Window) ---")
    print(classification_report(test[TARGET].astype(int), roll_pred))

    plot_sensor_streams(df)
    plot_anomaly_scores(test.reset_index(drop=True), scores)
    plot_comparison([p_b, r_b, f_b], [p_r, r_r, f_r])

    report_path = f"{RESULTS_DIR}/report.txt"
    with open(report_path, "w") as f:
        f.write("SKAB Digital Twin — Evaluation Report\n")
        f.write("="*45 + "\n\n")
        f.write(f"Baseline     — P: {p_b:.2f}  R: {r_b:.2f}  F1: {f_b:.2f}\n")
        f.write(f"Rolling Win  — P: {p_r:.2f}  R: {r_r:.2f}  F1: {f_r:.2f}\n\n")
        f.write(classification_report(test[TARGET].astype(int), roll_pred))
    print(f"\n[Evaluate] Report saved to {report_path}")

if __name__ == "__main__":
    run()
