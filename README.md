# Streaming Digital Twin Simulation Framework (DTSF)

This project implements a two-process streaming simulation system for validating stateful prognostic machine learning pipelines using synthetic telemetry replay.

---

## 🏗️ Actual System Architecture (Implementation-Level View)

```mermaid
graph LR

    subgraph "Process 1: Telemetry Emulator (FastAPI Server)"
        CSV["SKAB Dataset CSV"] --> API["sensor_server.py<br/>FastAPI Gateway"]
        API --> ENDPOINT["/telemetry/{tick_id}<br/>HTTP JSON Response"]
    end

    subgraph "Network Layer (Simulated IIoT Link)"
        ENDPOINT --> HTTP["HTTP Polling Interface<br/>requests.get()"]
    end

    subgraph "Process 2: Streaming Inference Engine"
        HTTP --> LOOP["run_pipeline.py<br/>Infinite Event Loop"]
        LOOP --> BUF["deque Sliding Window<br/>State Memory"]
        BUF --> FE["Real-time Feature Engineering<br/>(mean, std, diff)"]
        FE --> MODEL["Isolation Forest<br/>Anomaly Detection"]
        MODEL --> STATE["SKABAssetTwin<br/>Health State Tracker"]
        STATE --> DASH["Console + Streamlit Dashboard"]
    end

    style API fill:#e1f5fe,stroke:#01579b
    style LOOP fill:#f3e5f5,stroke:#6a1b9a
    style MODEL fill:#fff3e0,stroke:#e65100
