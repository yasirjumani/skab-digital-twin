import numpy as np

class AssetTopology:
    def __init__(self):
        self.dependencies = {
            "Valve_Inlet": ["Water_Pump"],
            "Water_Pump": ["Main_Pipe", "Bypass_Valve"],
            "Main_Pipe": ["Filter_Unit"],
            "Filter_Unit": ["Discharge_Tank"]
        }
        self.sensor_to_asset = {
            "Inlet_Pressure": "Valve_Inlet",
            "Vibration_Triaxial": "Water_Pump",
            "Current_Amps": "Water_Pump",
            "Flow_Rate": "Main_Pipe",
            "Differential_Pressure": "Filter_Unit",
            "Temperature": "Filter_Unit"
        }

class SKABAssetTwin:
    def __init__(self, asset_id="SKAB_Pump_System"):
        self.asset_id = asset_id
        self.topology = AssetTopology()
        
        # State Variables
        self.health_score = 100.0
        self.operating_state = "NOMINAL"
        
        # Tracking buffers for Statistical Process Control (SPC) & Trends
        self.score_history = []
        self.ewma_score = None
        self.lambda_ewma = 0.15  # Smoothing factor
        self.telemetry_history = []
        self.health_history = []
        
    def update(self, sensor_data_dict, raw_anomaly_score):
        """Processes a live tick using an EWMA statistical process control architecture."""
        self.telemetry_history.append(sensor_data_dict)
        self.score_history.append(raw_anomaly_score)
        
        if len(self.telemetry_history) > 1000:
            self.telemetry_history.pop(0)
            self.score_history.pop(0)
            
        # 1. Compute EWMA: S_t = \lambda * Y_t + (1 - \lambda) * S_{t-1}
        if self.ewma_score is None:
            self.ewma_score = raw_anomaly_score
        else:
            self.ewma_score = (self.lambda_ewma * raw_anomaly_score) + ((1 - self.lambda_ewma) * self.ewma_score)
            
        # 2. Dynamic Statistical Thresholding (SPC $3\sigma$ control limit approach)
        if len(self.score_history) > 30:
            mean_score = np.mean(self.score_history[-100:])
            std_score = np.std(self.score_history[-100:])
            ucl = mean_score + (3 * std_score)
            lcl = mean_score - (2.5 * std_score) # Lower control limit focus for Isolation Forest scores
            
            if self.ewma_score < lcl:
                self.operating_state = "🔴 HIGH-CONFIDENCE ALERT"
            elif self.ewma_score < (lcl + 0.02):
                self.operating_state = "🟡 LOW-CONFIDENCE WARNING"
            else:
                self.operating_state = "🟢 NOMINAL OPERATION"
        else:
            self.operating_state = "🟢 NOMINAL OPERATION"
            
        # 3. Multi-Factor Defensible Health Formulation
        self._calculate_composite_health(raw_anomaly_score, sensor_data_dict)
        return self.operating_state

    def _calculate_composite_health(self, raw_score, metrics):
        """Calculates a rigorous multi-factor degradation index."""
        # Factor A: Current Anomaly Severity (Normalized between 0 and 1)
        # Isolation Forest outputs highly anomalous scores near negative values (-0.2 to -0.4)
        anom_comp = max(0.0, min(1.0, (raw_score + 0.5) / 0.5)) * 100
        
        # Factor B: Cumulative Stress Component (Degradation curve based on history length)
        anomaly_count = sum(1 for s in self.score_history[-50:] if s < -0.03)
        degrad_comp = max(0.0, 1.0 - (anomaly_count / 50.0)) * 100
        
        # Factor C: Trend Vector Component (Slope of the last 20 frames)
        if len(self.score_history) >= 20:
            slope = np.polyfit(range(20), self.score_history[-20:], 1)[0]
            trend_comp = 100.0 if slope >= 0 else max(0.0, 100.0 + (slope * 500))
        else:
            trend_comp = 100.0
            
        # Factor D: Operational Load Constraint (Physics boundaries verification)
        # Simulating a high-temperature/flow penalty constraint
        flow = metrics.get("Flow_Rate", 1.0)
        load_comp = 100.0 if flow <= 1.5 else max(0.0, 100.0 - (flow - 1.5) * 50)
        
        # Composite Math Formulation: 40% Anomaly + 30% Degradation + 20% Trend + 10% Load
        self.health_score = (0.40 * anom_comp) + (0.30 * degrad_comp) + (0.20 * trend_comp) + (0.10 * load_comp)
        self.health_history.append(self.health_score)
        if len(self.health_history) > 500:
            self.health_history.pop(0)

    def diagnostic_root_cause(self, anomalous_features):
        """Root Cause Analysis utilizing Topologic Suspect Scoring Matrix."""
        suspect_components = []
        for feature in anomalous_features:
            clean_feat = next((k for k in self.topology.sensor_to_asset.keys() if k in feature), None)
            if clean_feat:
                suspect_components.append(self.topology.sensor_to_asset[clean_feat])
                
        if not suspect_components:
            return {"Primary Suspect": "Unknown System Drift", "Confidence": 0.50}
            
        unique, counts = np.unique(suspect_components, return_counts=True)
        probabilities = counts / counts.sum()
        best_idx = np.argmax(probabilities)
        
        return {
            "Primary Suspect": unique[best_idx],
            "Confidence": float(probabilities[best_idx]),
            "All Suspected Nodes": list(unique)
        }
