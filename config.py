# ============================================================
# SKAB Digital Twin — Central Configuration
# ============================================================

DATA_PATH = "data/other/1.csv"
SEPARATOR = ";"
DATETIME_COL = "datetime"

FEATURES = [
    "Accelerometer1RMS",
    "Accelerometer2RMS",
    "Current",
    "Pressure",
    "Temperature",
    "Thermocouple",
    "Voltage",
    "Volume Flow RateRMS"
]

TARGET = "anomaly"

# Feature engineering
WINDOW_SIZE = 5

# Isolation Forest
CONTAMINATION = 0.08
N_ESTIMATORS = 150
RANDOM_STATE = 42

# Statistical Process Control
Z_THRESHOLD = 2.0

# Ensemble debouncing
DEBOUNCE_SIZE = 3

# Calibration split
CALIBRATION_ROWS = 200

# Output paths
RESULTS_DIR = "results"
