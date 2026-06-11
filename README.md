# Streaming Digital Twin Simulation Framework (DTSF)

A research-grade simulation framework for validating stateful prognostic machine learning pipelines. 

## 1. System Conceptual Model
Our framework adheres to the standard predictive maintenance streaming architecture, decoupling data ingestion from prognostic logic.

| Layer | Responsibility | Mechanism |
| :--- | :--- | :--- |
| **Data Emulation** | Telemetry source replay | Stateless HTTP Gateway |
| **Orchestration** | Temporal event alignment | Tick-based Event Loop |
| **Stateful Processing** | Temporal context preservation | Sliding Window (`deque`) |
| **Decision Layer** | Health Index (HI) derivation | Anomaly Scoring -> Normalization |

## 2. Implementation Specification
To realize this conceptual model, the system is engineered as a decoupled, two-process simulation.

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
