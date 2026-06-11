# Streaming Digital Twin Simulation Framework (DTSF)

This project focuses on architectural correctness of streaming ML systems rather than physical system fidelity or industrial deployment.

A modular, event-driven emulation environment for streaming prognostic health monitoring (PHM) and anomaly detection in industrial assets. This project provides a robust, decoupled architecture for simulating telemetry pipelines and validating streaming ML workflows.

---

## 🏗️ Architectural Overview
The system is built on a **Producer-Consumer microservice pattern**, designed to emulate the separation between physical IoT edge devices and back-end analytics engines.

* **IIoT Gateway (Producer):** A decoupled API service that transforms static datasets (e.g., SKAB) into asynchronous, event-driven telemetry streams.
* **Stateful Inference Pipeline (Consumer):** An autonomous engine that maintains local temporal context via sliding window buffers, performing real-time inference on incoming sensor packets.

## 🛠️ Engineering Highlights
* **Streaming ML Workflow:** Implements online inference over sequential event ingestion using rolling statistical feature windows (mean, std, diff) to provide temporal context for time-series modeling.
* **Decoupled Architecture:** Simulates IoT-style separation between telemetry generation and inference using a network-style API interface.
* **Heuristic Prognostic Health Modeling:** Maps anomaly scores to a normalized health index to simulate degradation behavior in industrial assets.
* **Modular Pipeline Design:** Separates ingestion, feature engineering, state management, and inference into independent components with a non-blocking visualization layer.

## System Model
The framework employs a **Decoupled Sequential Inference** model:
* **Ingestion:** Data is ingested via a REST API, emulating the transmission of telemetry from a physical edge device to a gateway.
* **Feature Engineering:** Features are computed on a sliding temporal buffer, preserving local sequential dependency.
* **Inference:** A pre-fitted anomaly detection model is applied to the buffered state, producing a real-time anomaly score.
* **Prognostics:** Anomaly scores are transformed into a normalized health index, representing the asset's degradation trajectory.

## 📋 Technical Scope
This framework is designed as an architectural simulation environment for:
* Streaming inference validation under sequential time-series inputs.
* System design prototyping for decoupled telemetry and analytics pipelines.
* Stateful ML pipeline experimentation for predictive maintenance logic.

**Non-goals:**
* Real-time industrial deployment.
* Physical sensor integration.
* Physics-accurate system modeling.
