import pandas as pd
from config import FEATURES, WINDOW_SIZE

def add_rolling_features(df):
    df = df.copy()
    for col in FEATURES:
        df[f"{col}_mean"] = df[col].rolling(WINDOW_SIZE, min_periods=1).mean()
        df[f"{col}_std"] = df[col].rolling(WINDOW_SIZE, min_periods=1).std().fillna(0)
        df[f"{col}_diff"] = df[col].diff().fillna(0)
    print(f"[Features] Added rolling mean/std/diff for {len(FEATURES)} sensors")
    return df

def get_feature_columns():
    base = FEATURES
    rolling = [f"{c}_{s}" for c in FEATURES for s in ["mean", "std", "diff"]]
    return base + rolling
