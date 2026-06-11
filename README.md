# Streaming Digital Twin Simulation Framework (DTSF)

A research-grade simulation framework for validating stateful prognostic machine learning pipelines. This project focuses on the architectural decoupling of data emulation and streaming inference.

---

## 🏗️ Architectural Overview
We employ a tiered hierarchy to separate concerns:
1. **Data Emulation:** Provides raw telemetry via a stateless gateway.
2. **Orchestration:** Manages the sequential flow of time-series events.
3. **Stateful Processing:** Maintains temporal memory for predictive analysis.
4. **Decision Layer:** Translates model outputs into actionable health metrics.

```mermaid
graph TD
    subgraph L1 [Data Emulation Layer]
        DS[SKAB Dataset] --> SE[Telemetry Producer]
    end
    subgraph L2 [Streaming Orchestration Layer]
        SE --> SC[Stream Controller]
    end
    subgraph L3 [Stateful Processing Layer]
        SC --> SB[Temporal Sliding Window]
        SB --> FE[Feature Engineering]
        FE --> INF[Anomaly Detection Engine]
    end
    subgraph L4 [Decision Layer]
        INF --> HI[Prognostic Health Index]
        HI --> UI[Streamlit Dashboard]
    end
