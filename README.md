# 🏭 SKAB Asset Digital Twin Control Center (V2.1)

A modular, production-ready Industry 4.0 Predictive Maintenance Digital Twin platform built for industrial water treatment systems. This platform goes beyond static machine learning predictions by maintaining a living, state-aware software representation of physical assets using the SKAB (Water Pump Anomaly Detection) dataset.

The system tightly couples unsupervised machine learning edge models with dynamic statistical process control filters, physical fluid affinity surrogates, topologic asset graphs, and adaptive hybrid prognostics.

---

## 🧬 Key Architectural Features

### 1. Persistent State Engine & SPC Layer
Instead of running isolated model inferences (`predict(X)`), the system leverages a continuous state machine (`SKABAssetTwin`). 
* **Noise Mitigation:** Implements an **Exponentially Weighted Moving Average (EWMA)** smoothing filter onto incoming anomaly vectors to eliminate false-alarm toggling and UI flickering.
* **Dynamic Control Limits:** Replaces hardcoded detection boundaries with an automated **Statistical Process Control (SPC) $3\sigma$ Lower Control Limit** approach to dynamically isolate anomalous deviations.

### 2. Multi-Factor Health Indexing
Asset degradation is evaluated through a defensible, multi-variable objective function rather than simple counters:
$$\text{Health} = 0.40 \cdot H_{\text{anomaly}} + 0.30 \cdot H_{\text{degradation}} + 0.20 \cdot H_{\text{trend}} + 0.10 \cdot H_{\text{load}}$$
* **$H_{\text{anomaly}}$:** Real-time geometric anomaly vector distance from the steady-state baseline.
* **$H_{\text{degradation}}$:** Cumulative micro-stress persistence lengths over time.
* **$H_{\text{trend}}$:** Linear trend line slopes tracking the velocity of deterioration.
* **$H_{\text{load}}$:** Real-time operational boundary violations (e.g., thermal/flow limit penalties).

### 3. Adaptive Hybrid Prognostics (Remaining Useful Life)
The system calculates time-to-failure (TTF) targeting a critical threshold ($H = 25\%$) using an analytical hybrid mechanism:
* **Primary Model:** Fits recent history vectors into a log-transformed exponential decay matrix: $\ln(y) = \ln(H_0) - \alpha t$.
* **Fallback Model:** If a sudden transient shock induces sharp drops before the exponential window can fully calibrate ($\alpha \le 0.0001$), the system dynamically swops to a **Linear Velocity Delta ($\Delta H / \Delta t$)** tracking equation to guarantee continuous predictive integrity.

### 4. Physics-Informed "What-If" Simulation Sandbox
Integrates hydromechanical engineering affinity laws directly into the digital shadow. When testing alternative operational inputs, the surrogate simulator maps out fluid profile modifications via quadratic pipeline relations:
$$\Delta P_{\text{simulated}} = \Delta P_{\text{base}} \cdot \left(\frac{Q_{\text{simulated}}}{Q_{\text{base}}}\right)^2$$
This allows operators to verify internal backpressure constraints, safety disk tolerances, and pipe wall friction limits virtually before adjusting the live physical machinery.

### 5. Topology-Driven Root Cause Analysis (RCA)
Maintains a structural directed acyclic dependencies graph mapping system sensors directly to physical operational blocks (`Valve_Inlet`, `Water_Pump`, `Filter_Unit`, `Discharge_Tank`). When anomalies bridge limits, a topologic suspect scoring matrix computes a probability index identifying the primary subsystem responsible, matching it directly to highly specific prescriptive industrial protocol instructions.

---

## 📊 Dashboard Preview & Telemetry UI

The Streamlit control room utilizes an advanced non-blocking session-state loop architecture. Instead of putting the main dashboard thread into an infinite UI-freezing loop, it handles exactly one sensor frame per script execution lifecycle, rendering flawless real-time charts, asset dependencies data graphs, simulator labs, and operational alarms without any interface flickering.

---

## 📁 Repository Structure

```text
├── twin/                  # Data Ingestion and Feature Engineering pipelines
│   ├── ingestion.py       # SKAB dataset processing handlers
│   └── features.py        # Engineered rolling statistical variables
├── twin_core/             # Advanced Digital Twin Engine Core
│   ├── engine.py          # State machine, SPC EWMA filters, and Asset Topology Graph
│   └── analytics.py       # Log-exponential RUL prognostics & Physics What-If simulator
├── web_app.py             # Non-blocking Streamlit UI Control Room Dashboard
├── config.py              # Global architectural configuration hyper-parameters
└── requirements.txt       # Dependencies manifest
