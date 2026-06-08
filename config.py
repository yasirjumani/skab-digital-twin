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
WINDOW_SIZE = 5
CONTAMINATION = 0.12
N_ESTIMATORS = 200
RANDOM_STATE = 42
Z_THRESHOLD = 1.5
DEBOUNCE_SIZE = 1
CALIBRATION_ROWS = 200
RESULTS_DIR = "results"
