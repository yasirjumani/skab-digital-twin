import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from config import CONTAMINATION, N_ESTIMATORS, RANDOM_STATE, Z_THRESHOLD, FEATURES

class IsolationForestEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=CONTAMINATION,
            n_estimators=N_ESTIMATORS,
            random_state=RANDOM_STATE
        )

    def fit(self, X):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        print("[Engine 1] Isolation Forest trained")

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)
        scores = self.model.decision_function(X_scaled)
        return (preds == -1).astype(int), scores

class SPCEngine:
    def __init__(self):
        self.means = {}
        self.stds = {}

    def fit(self, df):
        for col in FEATURES:
            self.means[col] = df[col].mean()
            self.stds[col] = df[col].std() if df[col].std() > 0 else 1e-5
        print(f"[Engine 2] SPC calibrated at {Z_THRESHOLD} sigma")

    def predict_tick(self, tick_dict):
        for col in FEATURES:
            z = abs(tick_dict[col] - self.means[col]) / self.stds[col]
            if z > Z_THRESHOLD:
                return 1
        return 0
