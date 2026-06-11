import time
import pandas as pd
from fastapi import FastAPI
import uvicorn
import config

app = FastAPI(
    title="Industrial IoT Edge Gateway Emulation Server",
    description="Emulates network-isolated hardware asset telemetry broadcasting over HTTP"
)

# Load the core SKAB reference asset file
try:
    df_raw = pd.read_csv(config.DATA_PATH, sep=';', parse_dates=['datetime'])
except (ValueError, KeyError):
    df_raw = pd.read_csv(config.DATA_PATH)

drop_cols = ['datetime', 'anomaly', 'changepoint']
sensor_cols = [col for col in df_raw.columns if col not in drop_cols]
telemetry_records = df_raw[sensor_cols].to_dict(orient='records')

@app.get("/api/v1/telemetry/{tick_id}")
def get_sensor_telemetry(tick_id: int):
    # Emulate a continuous circular factory loop asset cycle
    index = tick_id % len(telemetry_records)
    return {
        "status": "ONLINE",
        "emulated_timestamp": str(pd.Timestamp.now()),
        "network_tick": tick_id,
        "payload": telemetry_records[index]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
