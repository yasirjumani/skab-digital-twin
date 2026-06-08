import pandas as pd
from config import DATA_PATH, SEPARATOR, DATETIME_COL, FEATURES, TARGET

def load_data():
    df = pd.read_csv(DATA_PATH, sep=SEPARATOR, parse_dates=[DATETIME_COL])
    print(f"[Ingestion] Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"[Ingestion] Anomaly rate: {df[TARGET].mean()*100:.1f}%")
    return df

def get_stream(df, start=200, end=None):
    subset = df.iloc[start:end] if end else df.iloc[start:]
    for _, row in subset.iterrows():
        yield row[FEATURES].to_dict(), row[DATETIME_COL], int(row[TARGET])
