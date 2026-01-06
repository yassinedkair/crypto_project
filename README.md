# 🚀 Real-Time Bitcoin AI Predictor (End-to-End MLOps Pipeline)

## 📖 Overview
This project is a fully automated **Real-Time Data Engineering & ML Pipeline** designed to predict Bitcoin prices.

Unlike simple scrapers, this system uses **Apache Kafka** for streaming data ingestion, stores it in **PostgreSQL**, automates model retraining using **Apache Airflow**, and visualizes live insights (Price, RSI, Predictions) via an interactive **Streamlit Dashboard**.

## ⚠️ Project Status
* **Model:** **Random Forest Regressor** (Advanced Logic).
* **Strategy:** Scalping (Short-term prediction: T+1 minute).
* **Disclaimer:** This project is a demonstration of **DevOps, Data Engineering, and MLOps** skills. While the model uses advanced indicators (RSI, Lag Features), crypto markets are unpredictable. Do not use this for real financial trading.

## 🛠️ Tech Stack
* **Streaming:** Apache Kafka (Producer/Consumer pattern)
* **Database:** PostgreSQL (Persistent storage)
* **Orchestration:** Apache Airflow (Automated periodic retraining)
* **Machine Learning:** Scikit-learn (Random Forest Regressor)
* **Visualization:** Streamlit (Interactive Real-Time Dashboard)
* **Containerization:** Docker & Docker Compose (Full isolation)

## ⚙️ Workflow Architecture
1. **Data Ingestion (Producer):** Fetches live BTC/USD prices and pushes them to a Kafka Topic.
2. **Data Processing (Consumer):** Consumes messages from Kafka and stores them in a PostgreSQL database.
3. **ML Training (Airflow):** A scheduled DAG retrains the **Random Forest** model every 10 minutes on the latest data to adapt to market trends.
4. **Inference & UI (Streamlit):**
    * Loads the latest model.
    * Calculates technical indicators (RSI).
    * Displays real-time price, AI predictions, and Buy/Sell signals.

## 🚀 How to Run

### Prerequisites
* Docker Desktop installed & running.
* Git installed.

### Steps
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yassinedkair/crypto_project.git](https://github.com/yassinedkair/crypto_project.git)
    cd crypto_project
    ```

2.  **Start the Services:**
    ```bash
    docker-compose up --build
    ```
    *(Wait a few minutes for Kafka, Postgres, and Airflow to initialize).*

3.  **Access the Applications:**
    * 📊 **Live Dashboard (Streamlit):** [http://localhost:8501](http://localhost:8501)
    * ⚙️ **Airflow UI (Pipeline Manager):** [http://localhost:8080](http://localhost:8080)
        * *Login:* `airflow` / `airflow`
        * *Action:* Trigger the `bitcoin_training_automated` DAG to build the initial model.

## 📸 Features
* **Real-Time Graph:** Live plotting of BTC prices vs AI Predictions.
* **RSI Indicator:** Gauge meter to detect Overbought/Oversold zones.
* **Automated MLOps:** The model gets smarter over time without manual intervention.

---
*Created by [Yassine]*