import time
import collections
import numpy as np
import pandas as pd
import config
from twin_core.engine import SKABAssetTwin
from sklearn.ensemble import IsolationForest

print("Initializing Stateful Streaming Simulator...")

# Load the CSV directly using the config path
try:
    df_raw = pd.read_csv(config.DATA_PATH, sep=';', parse_dates=['datetime'], index_col='datetime')
except (ValueError, KeyError):
    df_raw = pd.read_csv(config.DATA_PATH)

drop_cols = ['datetime', 'anomaly', 'changepoint']
sensor_cols = [col for col in df_raw.columns if col not in drop_cols]

# Instantiate the digital twin state machine
twin = SKABAssetTwin()

print("Calibrating baseline machine learning feature models...")
base_model = IsolationForest(contamination=0.1, random_state=42)

# Initialize the Stateful Stream Feature Queue matching your WINDOW_SIZE
stream_buffer = collections.defaultdict(lambda: collections.deque(maxlen=config.WINDOW_SIZE))

# Build temporary calibration data to prime the structure
init_features = []
for _, raw_row in df_raw.head(config.CALIBRATION_ROWS).iterrows():
    tick_dict = raw_row[sensor_cols].to_dict()
    processed_row_dict = {}
    for col in sensor_cols:
        processed_row_dict[col] = tick_dict[col]
        processed_row_dict[f"{col}_mean"] = tick_dict[col]
        processed_row_dict[f"{col}_std"] = 0.0
        processed_row_dict[f"{col}_diff"] = 0.0
    init_features.append(processed_row_dict)

X_init = pd.DataFrame(init_features)
base_model.fit(X_init)

print(f"Starting Stream Processing Loop (Window Size: {config.WINDOW_SIZE})...")
print("-" * 80)

# Simulate row-by-row live IoT data arrival
for timestamp, raw_row in df_raw.iterrows():
    tick_dict = raw_row[sensor_cols].to_dict()
    processed_row_dict = {}
    
    # Dynamically compute rolling window metrics on the fly
    for col in sensor_cols:
        current_val = tick_dict[col]
        stream_buffer[col].append(current_val)
        
        active_window = np.array(stream_buffer[col])
        
        processed_row_dict[col] = current_val
        processed_row_dict[f"{col}_mean"] = np.mean(active_window)
        processed_row_dict[f"{col}_std"] = np.std(active_window) if len(active_window) > 1 else 0.0
        processed_row_dict[f"{col}_diff"] = current_val - active_window[-2] if len(active_window) > 1 else 0.0

    # Convert the processed tick dictionary into a unified Pandas DataFrame row
    row_df = pd.DataFrame([processed_row_dict])
    
    # Wait until our rolling window buffer is fully primed before evaluating
    if len(active_window) < config.WINDOW_SIZE:
        continue
        
    # Generate the raw machine learning anomaly score required by your update method
    raw_anomaly_score = base_model.decision_function(row_df)[0]
    
    # Pass BOTH required positional arguments (the feature series and the raw score)
    twin.update(row_df.iloc[0], raw_anomaly_score)
    
    # Extract structural variables matched directly to your internal engine.py names
    current_health = twin.health_score
    current_state = getattr(twin, 'current_state', getattr(twin, 'state', 'NOMINAL'))
    current_ewma = getattr(twin, 'smooth_ewma_score', getattr(twin, 'ewma_score', raw_anomaly_score))
    
    # Output clean telemetry metrics directly to terminal logs
    print(f"Timestamp: {timestamp} | Health: {current_health:.2f}% | "
          f"EWMA: {current_ewma:.4f} | State: {current_state}")
    
    # Throttling tick delay for realistic simulation playback speed
    time.sleep(0.1)
