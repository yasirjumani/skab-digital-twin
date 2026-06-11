import time
from collections import deque
import pandas as pd
import numpy as np
from twin.ingestion import load_data, get_stream
from twin.features import get_feature_columns
from twin.models import IsolationForestEngine, SPCEngine
from twin.ensemble import EnsembleFusion
from config import FEATURES, CALIBRATION_ROWS, WINDOW_SIZE

def compute_live_features(window: deque) -> pd.DataFrame:
    """Compute rolling features from the current tick window."""
    buf = pd.DataFrame(list(window))
    row = {}
    for col in FEATURES:
        row[col] = buf[col].iloc[-1]
        row[f"{col}_mean"] = buf[col].mean()
        row[f"{col}_std"] = buf[col].std() if len(buf) > 1 else 0.0
        row[f"{col}_diff"] = buf[col].diff().iloc[-1] if len(buf) > 1 else 0.0
    return pd.DataFrame([row])

def run():
    print("\n=== SKAB Digital Twin — Live Streaming Pipeline ===\n")

    df = load_data()
    feat_cols = get_feature_columns()

    # Train on calibration data (using pre-computed rolling features)
    from twin.features import add_rolling_features
    df_feat = add_rolling_features(df)
    calib = df_feat.iloc[:CALIBRATION_ROWS]

    if_engine = IsolationForestEngine()
    spc_engine = SPCEngine()
    if_engine.fit(calib[feat_cols].fillna(0))
    spc_engine.fit(calib)

    fusion = EnsembleFusion()

    # Seed the rolling window with the last WINDOW_SIZE calibration rows
    seed_rows = df.iloc[CALIBRATION_ROWS - WINDOW_SIZE: CALIBRATION_ROWS]
    window = deque(
        [row[FEATURES].to_dict() for _, row in seed_rows.iterrows()],
        maxlen=WINDOW_SIZE
    )

    print("\n📡 Streaming live sensor ticks...\n")
    print(f"{'Timestamp':<22} | {'IF Score':>12} | State")
    print("-" * 70)

    for tick, timestamp, true_label in get_stream(df, start=CALIBRATION_ROWS, end=CALIBRATION_ROWS + 60):
        window.append(tick)
        X = compute_live_features(window)[feat_cols].fillna(0)

        if_pred_arr, scores = if_engine.predict(X)
        if_pred = int(if_pred_arr[0])
        spc_pred = spc_engine.predict_tick(tick)

        state, level = fusion.evaluate(if_pred, spc_pred)
        label = EnsembleFusion.state_label(state)
        score = scores[0]

        marker = " ← TRUE ANOMALY" if true_label == 1 else ""
        print(f"{str(timestamp):<22} | {score:>+.6f} | {label}{marker}")
        time.sleep(0.02)

    print("\n[Pipeline] Stream complete.")

if __name__ == "__main__":
    run()
