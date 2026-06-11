# Streaming Digital Twin Simulation Framework (DTSF)

A research-grade framework for validating stateful prognostic machine learning pipelines. This project demonstrates the transformation of an academic time-series analysis prototype into a modular, industrial-grade streaming architecture.

---

## 🚀 Engineering Evolution (Academic → Industrial)
This framework evolved from a static, monolithic notebook analysis into a production-ready system by focusing on three core engineering pillars:

* **From Batch to Streaming:** Migrated from offline batch processing to a real-time event-driven architecture.
* **Process Decoupling:** Implemented a two-process architecture (Producer/Consumer) using REST protocols, mimicking real-world edge-to-cloud telemetry ingestion.
* **Stateful Resilience:** Replaced stateless operations with a stateful sliding-window buffer (`collections.deque`), allowing for $O(1)$ complexity updates and real-time temporal feature extraction.
* **Prognostic Fidelity:** Shifted from binary anomaly detection to a continuous, normalized **Health Index (HI)**, providing meaningful degradation trends for predictive maintenance.

---

## 🏗️ Technical Architecture
We define our system through two complementary models:

### 1. System Conceptual Model (The Pattern)
| Layer | Responsibility | Mechanism |
| :--- | :--- | :--- |
| **Data Emulation** | Telemetry source replay | Stateless HTTP Gateway |
| **Orchestration** | Temporal event alignment | Tick-based Event Loop |
| **Stateful Processing** | Temporal context preservation | Sliding Window (`deque`) |
| **Decision Layer** | Health Index (HI) derivation | Anomaly Scoring -> Normalization |

### 2. Implementation Specification (The Reality)
The system operates as a decoupled, two-process simulation.
```mermaid
graph LR
    subgraph "Producer Process (FastAPI)"
        CSV["SKAB Dataset"] --> API["FastAPI Gateway"]
    end
    API -- "HTTP Polling (REST)" --> INF["Inference Engine (Loop)"]
    subgraph "Consumer Process (Inference Engine)"
        INF --> BUF["deque Window (State)"]
        BUF --> FE["Feature Engine"]
        FE --> MOD["Isolation Forest"]
        MOD --> HI["Health State Tracker"]
    end
