# Streaming Digital Twin Simulation Framework (DTSF)

A research-grade framework for validating stateful prognostic machine learning pipelines. This project demonstrates the transformation of an academic time-series analysis prototype into a modular, industrial-grade streaming architecture.

---

## 🚀 Engineering Evolution: Academic to Industrial
This framework evolved from a static, monolithic notebook analysis into a production-ready system by focusing on four core engineering pillars:

* **From Batch to Streaming:** Transitioned from offline static batch processing to a real-time, event-driven architecture.
* **Service Decoupling:** Implemented a dual-process architecture (Producer/Consumer) using REST protocols, mimicking real-world edge-to-cloud telemetry ingestion.
* **Stateful Resilience:** Replaced stateless operations with a stateful sliding-window buffer using `collections.deque`, enabling $O(1)$ complexity updates and real-time feature extraction.
* **Prognostic Fidelity:** Shifted from binary anomaly labels to a continuous, normalized **Health Index (HI)**, facilitating trend-based predictive maintenance.

---

## 🏗️ Technical Architecture

### 1. System Conceptual Model
| Layer | Responsibility | Mechanism |
| :--- | :--- | :--- |
| **Data Emulation** | Telemetry source replay | Stateless HTTP Gateway |
| **Orchestration** | Temporal event alignment | Tick-based Event Loop |
| **Stateful Processing** | Temporal context preservation | Sliding Window (`deque`) |
| **Decision Layer** | Health Index (HI) derivation | Anomaly Scoring -> Normalization |

### 2. Implementation Specification
The system is engineered as a decoupled, two-process simulation.

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
