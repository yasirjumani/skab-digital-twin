import streamlit as st
import subprocess

st.set_page_config(page_title="SKAB Digital Twin", layout="wide")
st.title("🏭 SKAB Digital Twin — Live Simulation")
st.markdown("Streaming real-time anomaly detection logs from `run_pipeline.py`...")

log_box = st.empty()
logs = []

process = subprocess.Popen(
    ["python3", "run_pipeline.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

for line in iter(process.stdout.readline, ''):
    logs.append(line.strip())
    if len(logs) > 30:
        logs.pop(0)
    log_box.code('\n'.join(logs), language='text')
