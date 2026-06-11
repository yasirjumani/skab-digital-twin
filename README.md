# Streaming Digital Twin Simulation Framework (DTSF)

This project implements a streaming digital twin simulation framework for validating stateful prognostic machine learning pipelines. The system is designed for architectural correctness in streaming ML systems, rather than physical deployment or cyber-physical integration.

---

## 🧠 Key Idea

DTSF simulates how industrial digital twin pipelines operate by reproducing:

- Event-driven telemetry streaming
- Stateful time-series processing
- Real-time feature extraction
- Online anomaly detection and prognostic health estimation

It is a **simulation-first architecture** used to validate streaming ML system design patterns.

---

## 🏗️ System Architecture

The framework is organized as a layered streaming pipeline:

```mermaid
graph LR

    subgraph "Data Emulation Layer"
        DS[SKAB Dataset\nReplay Source] --> SE[Telemetry Producer\nHTTP Gateway]
    end

    subgraph "Streaming Orchestration Layer"
        SE -- "Sequential Event Stream\n(Tick-Based Ingestion)" --> SC[Stream Controller\nEvent Loop / Scheduler]
    end

    subgraph "Stateful Processing Layer"
        SC --> SB[Temporal Sliding Window\nState Buffer]
        SB --> FE[Feature Engineering\n(Mean, Std, Delta)]
        FE --> INF[Anomaly Detection Model\n(e.g., Isolation Forest)]
    end

    subgraph "Decision Layer"
        INF --> HI[Prognostic Health Index\nComputation]
        HI --> UI[Streamlit Dashboard\nMonitoring Interface]
    end
