import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from twin.ingestion import load_data
from twin.features import add_rolling_features, get_feature_columns
from twin.visualizer import plot_sensor_streams, plot_anomaly_scores, plot_comparison
from config import FEATURES, TARGET, CALIBRATION_ROWS, RESULTS_DIR, N_ESTIMATORS, RANDOM_STATE

os.makedirs(RESULTS_DIR, exist_ok=True)

def best_threshold(scores, y_val):
    """Find threshold that maximises F1 on the VALIDATION set only."""
    best_f1, best_t = 0, 0
    for t in np.linspace(scores.min(), scores.max(), 200):
        pred = (scores < t).astype(int)
        _, _, f1, _ = precision_recall_fscore_support(
            y_val, pred, average="binary", zero_division=0)
        if f1 > best_f1:
            best_f1, best_t = f1, t
    return best_t

def run():
    print("\n=== SKAB Digital Twin — Evaluation Pipeline ===\n")
    df = load_data()
    
    n = len(df)
    val_start  = CALIBRATION_ROWS
    val_end    = CALIBRATION_ROWS + (n - CALIBRATION_ROWS) // 2
    
    train = df.iloc[:CALIBRATION_ROWS]
    val   = df.iloc[val_start:val_end]
    test  = df.iloc[val_end:].copy()
    
    y_val  = val[TARGET].astype(int).values
    y_test = test[TARGET].astype(int).values
    
    print(f"Split — train: {len(train)}  val: {len(val)}  test: {len(test)}")
    print(f"Anomaly rate — val: {y_val.mean()*100:.1f}%  test: {y_test.mean()*100:.1f}%\n")
    
    scaler1 = StandardScaler()
    X_train_base = scaler1.fit_transform(train[FEATURES].fillna(0))
    X_val_base   = scaler1.transform(val[FEATURES].fillna(0))
    X_test_base  = scaler1.transform(test[FEATURES].fillna(0))
    
    model1 = IsolationForest(n_estimators=N_ESTIMATORS, contamination="auto", random_state=RANDOM_STATE)
    model1.fit(X_train_base)
    
    scores_val_base  = model1.decision_function(X_val_base)
    scores_test_base = model1.decision_function(X_test_base)
    
    t_base    = best_threshold(scores_val_base, y_val)
    base_pred = (scores_test_base < t_base).astype(int)
    
    p_b, r_b, f_b, _ = precision_recall_fscore_support(
        y_test, base_pred, average="binary", zero_division=0)
    
    df_feat = add_rolling_features(df)
    feat_cols = get_feature_columns()
    
    train_feat = df_feat.iloc[:CALIBRATION_ROWS]
    val_feat   = df_feat.iloc[val_start:val_end]
    test_feat  = df_feat.iloc[val_end:].copy()
    
    scaler2 = StandardScaler()
    X_train_roll = scaler2.fit_transform(train_feat[feat_cols].fillna(0))
    X_val_roll   = scaler2.transform(val_feat[feat_cols].fillna(0))
    X_test_roll  = scaler2.transform(test_feat[feat_cols].fillna(0))
    
    model2 = IsolationForest(n_estimators=N_ESTIMATORS, contamination="auto", random_state=RANDOM_STATE)
    model2.fit(X_train_roll)
    
    scores_val_roll  = model2.decision_function(X_val_roll)
    scores_test_roll = model2.decision_function(X_test_roll)
    
    t_roll    = best_threshold(scores_val_roll, y_val)
    roll_pred = (scores_test_roll < t_roll).astype(int)
    
    p_r, r_r, f_r, _ = precision_recall_fscore_support(
        y_test, roll_pred, average="binary", zero_division=0)
    
    test["predicted_anomaly"] = roll_pred
    
    print("--- Baseline Isolation Forest (raw features, held-out test) ---")
    print(f"Precision: {p_b:.2f}  Recall: {r_b:.2f}  F1: {f_b:.2f}")
    
    print("\n--- Upgraded: Rolling Window Features (held-out test) ---")
    print(f"Precision: {p_r:.2f}  Recall: {r_r:.2f}  F1: {f_r:.2f}")
    
    print("\n--- Full Report (Rolling Window) ---")
    print(classification_report(y_test, roll_pred))
    
    try:
        plot_sensor_streams(df)
        plot_anomaly_scores(test.reset_index(drop=True), scores_test_roll)
        plot_comparison([p_b, r_b, f_b], [p_r, r_r, f_r])
    except Exception as e:
        print(f"\n[Visualizer Notice] Plots failed: {e}")
        
    report_path = f"{RESULTS_DIR}/report.txt"
    with open(report_path, "w") as f:
        f.write("SKAB Digital Twin — Evaluation Report\n")
        f.write("=" * 45 + "\n\n")
        f.write("Threshold selection: validation set (no leakage)\n")
        f.write(f"Split — train: {len(train)}  val: {len(val)}  test: {len(test)}\n\n")
        f.write(f"Baseline     — P: {p_b:.2f}  R: {r_b:.2f}  F1: {f_b:.2f}\n")
        f.write(f"Rolling Win  — P: {p_r:.2f}  R: {r_r:.2f}  F1: {f_r:.2f}\n\n")
        f.write(classification_report(y_test, roll_pred))
        
    print(f"\n[Evaluate] Report saved to {report_path}")

if __name__ == '__main__':
    run()
