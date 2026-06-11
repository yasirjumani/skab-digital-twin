import streamlit as st
import pandas as pd
import time
from twin.ingestion import load_data
from twin.features import add_rolling_features, get_feature_columns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from config import FEATURES, TARGET, CALIBRATION_ROWS, N_ESTIMATORS, RANDOM_STATE
from twin_core.engine import SKABAssetTwin
from twin_core.analytics import TwinAnalytics

st.set_page_config(page_title="SKAB Industry 4.0 Digital Twin", layout="wide")
st.title("🏭 SKAB Asset Digital Twin Control Center")
st.markdown("---")

@st.cache_resource
def initialize_ml_backends():
    df = load_data()
    df_feat = add_rolling_features(df)
    feat_cols = get_feature_columns()
    train_feat = df_feat.iloc[:CALIBRATION_ROWS]
    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_feat[feat_cols].fillna(0))
    model = IsolationForest(n_estimators=N_ESTIMATORS, contamination="auto", random_state=RANDOM_STATE)
    model.fit(X_train)
    return scaler, model, df_feat, feat_cols

scaler, model, data_stream, feat_cols = initialize_ml_backends()

if "twin" not in st.session_state:
    st.session_state.twin = SKABAssetTwin()
    st.session_state.analytics = TwinAnalytics(st.session_state.twin)
    st.session_state.current_index = CALIBRATION_ROWS
    st.session_state.is_running = False

twin = st.session_state.twin
analytics = st.session_state.analytics

st.sidebar.subheader("🕹️ Twin Execution Panel")
if st.sidebar.button("▶️ Start Sync Loop" if not st.session_state.is_running else "⏸️ Pause Sync Loop"):
    st.session_state.is_running = not st.session_state.is_running
    st.rerun()

sidebar_alert_container = st.sidebar.empty()

col_metrics, col_graph = st.columns([2, 1])
with col_metrics:
    st.subheader("📊 Real-Time Operations Telemetry")
    metric_health = st.empty()
    metric_state = st.empty()
    metric_rul = st.empty()

with col_graph:
    st.subheader("🧬 Digital Asset Graph Matrix")
    st.json(twin.topology.dependencies)

st.markdown("---")
st.subheader("🧪 What-If Stress-Testing Simulator Labs")
sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    sim_flow = st.slider("Modify System Input Flow Target Scaling Factor", 0.5, 2.0, 1.0)
with sim_col2:
    if st.button("Execute Virtual Physics Simulation Task"):
        results = analytics.simulate_what_if({"Flow_Rate": sim_flow})
        st.write(results)

st.markdown("---")
st.subheader("📟 Real-Time Asset Stream Logs")
log_area = st.empty()

# Persistent metric rendering engine frames
metric_health.metric(label="💘 Dynamic Composite Asset Health", value=f"{twin.health_score:.2f} %")
metric_state.metric(label="⚙️ Current Twin Operations Matrix Status", value=twin.operating_state)
metric_rul.metric(label="⏳ Predictive Prognostics RUL Curve Matrix", value=analytics.estimate_remaining_useful_life())

if st.session_state.is_running and st.session_state.current_index < len(data_stream):
    idx = st.session_state.current_index
    row = data_stream.iloc[idx]
    
    X_scaled = scaler.transform(pd.DataFrame([row[feat_cols]]).fillna(0))
    raw_score = model.decision_function(X_scaled)[0]
    
    # Delegate tracking thresholds internally to our state engine
    status = twin.update(row[FEATURES], raw_score)
    rul_prediction = analytics.estimate_remaining_useful_life()
    
    metric_health.metric(label="💘 Dynamic Composite Asset Health", value=f"{twin.health_score:.2f} %")
    metric_state.metric(label="⚙️ Current Twin Operations Matrix Status", value=twin.operating_state)
    metric_rul.metric(label="⏳ Predictive Prognostics RUL Curve Matrix", value=rul_prediction)
    
    if "ALERT" in status or "WARNING" in status:
        active_anoms = [c for c in feat_cols if abs(row[c]) > 1.2]
        if not active_anoms:
            active_anoms = ["Flow_Rate", "Temperature"]
            
        diag = twin.diagnostic_root_cause(active_anoms)
        recs = analytics.generate_prescriptive_actions(diag)
        
        with sidebar_alert_container.container():
            st.error(f"🚨 Fault Implicated! Subsystem Target: {diag['Primary Suspect']}")
            st.write(f"**Calculated Core Confidence:** {diag['Confidence']*100:.1f}%")
            st.write("**Prescriptive Diagnostics Protocols:**")
            for r in recs:
                st.markdown(r)
    else:
        sidebar_alert_container.empty()
        
    log_area.text(f"Timestamp: {row.name} | Raw IF-Score: {raw_score:+.4f} | Smooth EWMA: {twin.ewma_score:+.4f} | State: {status}")
    
    st.session_state.current_index += 1
    time.sleep(0.04)
    st.rerun()
