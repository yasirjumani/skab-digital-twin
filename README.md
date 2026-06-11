# Streaming Digital Twin Simulation Framework (DTSF)

This project implements a streaming digital twin simulation framework for validating stateful prognostic machine learning pipelines. The system is designed for architectural correctness in streaming ML systems, rather than physical deployment or cyber-physical integration.

---

## 🏗️ System Architecture

The framework is organized as a layered streaming pipeline:

```mermaid
graph LR

    subgraph "Data Emulation Layer"
        DS["SKAB Dataset<br/>Replay Source"] --> SE["Telemetry Producer<br/>HTTP Gateway"]
    end

    subgraph "Streaming Orchestration Layer"
        SE -- "Sequential Event Stream<br/>(Tick-Based Ingestion)" --> SC["Stream Controller<br/>Event Loop / Scheduler"]
    end

    subgraph "Stateful Processing Layer"
        SC --> SB["Temporal Sliding Window<br/>State Buffer"]
        SB --> FE["Feature Engineering<br/>(Mean, Std, Delta)"]
        FE --> INF["Anomaly Detection Model<br/>(e.g., Isolation Forest)"]
    end

    subgraph "Decision Layer"
        INF --> HI["Prognostic Health Index<br/>Computation"]
        HI --> UI["Streamlit Dashboard<br/>Monitoring Interface"]
    end
