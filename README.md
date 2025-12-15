# 📈 Real-Time Crypto Price Predictor (1-Min Interval)

## 📖 Overview
This project is an automated **End-to-End Data Pipeline** designed to fetch, process, and predict cryptocurrency prices for the **next minute**.

The system scrapes/fetches live data, cleans it, trains a Machine Learning model, and generates a visualization graph of the price trends. The entire workflow is orchestrated using **Apache Airflow** and runs inside **Docker** containers.

## ⚠️ Project Status & Disclaimer
* **Current Model:** Simple **Linear Regression**.
* **Accuracy:** Since crypto markets are highly volatile and non-linear, this model serves primarily as a **Proof of Concept (PoC)** to demonstrate the automated pipeline architecture (Data Engineering & MLOps skills) rather than for accurate financial trading.

## 🛠️ Tech Stack
* **Orchestration:** Apache Airflow
* **Containerization:** Docker & Docker Compose
* **Language:** Python
* **Machine Learning:** Scikit-learn (Linear Regression)
* **Visualization:** Matplotlib (Price Graph generation)

## ⚙️ Workflow Architecture
1. **Data Ingestion:** Fetches live crypto prices from the source.
2. **Preprocessing:** Cleans data and prepares features.
3. **Training:** Retrains the Linear Regression model on the latest data.
4. **Prediction:** Predicts the price for the next minute (T+1).
5. **Visualization:** Generates and saves a graph of the price movements.

## 🚀 How to Run

### Prerequisites
* Docker Desktop installed.
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

3.  **Access Airflow:**
    * Go to `http://localhost:8080`.
    * Trigger the main DAG to start the fetching and prediction loop.

---
*Created by [Yassine]*
