# Streaming Digital Twin Simulation Framework (DTSF)

A research-grade simulation framework for validating stateful prognostic machine learning pipelines. The system focuses on decoupled streaming architecture design rather than physical system integration.

---

## 🏗️ Architectural Overview

The system is implemented as a **two-process streaming simulation pipeline** that emulates industrial telemetry flows using event-driven replay of time-series data.

### 1. Data Emulation Layer
- SKAB dataset is replayed as synthetic telemetry
- Exposed via a FastAPI HTTP gateway
- Provides time-indexed sensor readings via `/telemetry/{tick_id}`

### 2. Streaming Orchestration Layer
- A tick-based execution loop drives sequential data ingestion
- HTTP polling (`requests.get`) simulates networked IoT communication
- Ensures ordered event streaming across time

### 3. Stateful Processing Layer
- Maintains temporal memory using sliding window buffers (`deque`)
- Computes real-time statistical features:
  - Mean (μ)
  - Standard deviation (σ)
  - Temporal delta (Δ)
- Feeds engineered features into anomaly detection model

### 4. Decision Layer
- Uses anomaly scores from Isolation Forest model
- Maps outputs into a normalized health index
- Tracks degradation trends over time for prognostic interpretation

---

## ⚙️ System Execution Model

- Producer: FastAPI telemetry server (sensor emulation)
- Consumer: Python streaming inference engine
- Communication: HTTP-based polling interface
- Execution: infinite event loop (tick-driven simulation)
