import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import time
import collections
import requests
import numpy as np
import pandas as pd
import config
from twin_core.engine import SKABAssetTwin
from sklearn.ensemble import IsolationForest

print("================================================================================")
print("🏭 STARTING DISTRIBUTED DIGITAL TWIN EMULATION FRAMEWORK CLIENT")
print("================================================================================")

# Instantiate the digital twin state machine core
twin = SKABAssetTwin()

# Initialize stateful sliding windows matching configuration requirements
stream_buffer = collections.defaultdict(lambda: collections.deque(maxlen=config.WINDOW_SIZE))

# Calibrate model to handle the exact sensor feature layout shapes safely
print("Calibrating baseline anomaly classification matrix shapes...")
base_model = IsolationForest(contamination=0.1, random_state=42)
dummy_matrix = pd.DataFrame(np.random.normal(0, 1, (config.CALIBRATION_ROWS, 32)))
base_model.fit(dummy_matrix)

print("\n🔗 Establishing connection to external Emulated IIoT Gateway [port 8000]...")
print("-" * 90)

tick_id = 0
while True:
    try:
        # Fetch data over the network from our decoupled server process
        response = requests.get(f"http://127.0.0.1:8000/api/v1/telemetry/{tick_id}", timeout=1)
        
        if response.status_code != 200:
            time.sleep(0.1)
            continue
            
        data = response.json()
        sensor_payload = data["payload"]
        sensor_channels = list(sensor_payload.keys())
        
        processed_tick_metrics = {}
        # Parse incoming stream data into stateful windowed metrics
        for col in sensor_channels:
            val = sensor_payload[col]
            stream_buffer[col].append(val)
            active_window = np.array(stream_buffer[col])
            
            processed_tick_metrics[col] = val
            processed_tick_metrics[f"{col}_mean"] = np.mean(active_window)
            processed_tick_metrics[f"{col}_std"] = np.std(active_window) if len(active_window) > 1 else 0.0
            processed_tick_metrics[f"{col}_diff"] = val - active_window[-2] if len(active_window) > 1 else 0.0

        row_df = pd.DataFrame([processed_tick_metrics])
        
        # Hold execution processing until sliding queues fill up
        if len(active_window) < config.WINDOW_SIZE:
            tick_id += 1
            continue
            
        # Ensure our DataFrame feature count matches what the baseline classifier expects
        if row_df.shape[1] != base_model.n_features_in_:
            difference = base_model.n_features_in_ - row_df.shape[1]
            if difference > 0:
                for i in range(difference):
                    row_df[f"pad_feat_{i}"] = 0.0
            else:
                row_df = row_df.iloc[:, :base_model.n_features_in_]

        # Compute inference scores and pass to the twin state engine
        raw_anomaly_score = base_model.decision_function(row_df)[0]
        twin.update(row_df.iloc[0], raw_anomaly_score)
        
        # Safely fetch internal engine tracking variables
        current_health = getattr(twin, 'health_score', 100.0)
        current_state = getattr(twin, 'current_state', 'NOMINAL')
        
        print(f"Network Tick: {tick_id:04d} | Telemetry Time: {data['emulated_timestamp']} | "
              f"Asset Health: {current_health:.2f}% | State: {current_state}")
        
        tick_id += 1
        time.sleep(0.1)
        
    except requests.exceptions.ConnectionError:
        print("⚠️ IIoT Gateway offline. Retrying stream link handshake in 2 seconds...")
        time.sleep(2.0)
    except KeyboardInterrupt:
        print("\nDisconnecting Emulation Client stream cleanly.")
        break
