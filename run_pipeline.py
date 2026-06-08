import time
from twin.ingestion import load_data, get_stream
from twin.features import add_rolling_features
from twin.models import IsolationForestEngine, SPCEngine
from twin.ensemble import EnsembleFusion
from config import FEATURES, CALIBRATION_ROWS

def run():
    print("\n=== SKAB Digital Twin — Live Streaming Pipeline ===\n")
    df = load_data()
    df_feat = add_rolling_features(df)

    from twin.features import get_feature_columns
    feat_cols = get_feature_columns()

    # Train on calibration data
    if_engine = IsolationForestEngine()
    spc_engine = SPCEngine()
    calib = df_feat.iloc[:CALIBRATION_ROWS]
    if_engine.fit(calib[feat_cols].fillna(0))
    spc_engine.fit(calib)

    fusion = EnsembleFusion()

    print("\n📡 Streaming live sensor ticks...\n")
    print(f"{'Timestamp':<22} | {'IF Score':>12} | State")
    print("-" * 70)

    for tick, timestamp, true_label in get_stream(df, start=CALIBRATION_ROWS, end=CALIBRATION_ROWS+60):
        import pandas as pd
        import numpy as np
        row_df = pd.DataFrame([tick])
        for col in FEATURES:
            row_df[f"{col}_mean"] = tick[col]
            row_df[f"{col}_std"]  = 0.0
            row_df[f"{col}_diff"] = 0.0
        X = row_df[feat_cols].fillna(0)
        if_pred_arr, scores = if_engine.predict(X)
        if_pred = int(if_pred_arr[0])
        spc_pred = spc_engine.predict_tick(tick)
        state, level = fusion.evaluate(if_pred, spc_pred)
        label = EnsembleFusion.state_label(state)
        score = scores[0]
        marker = " ← TRUE ANOMALY" if true_label == 1 else ""
        print(f"{str(timestamp):<22} | {score:>+.6f}   | {label}{marker}")
        time.sleep(0.02)

    print("\n[Pipeline] Stream complete.")

if __name__ == "__main__":
    run()
