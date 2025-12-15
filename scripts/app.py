import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from sqlalchemy import create_engine
import time

# --- CONFIGURATION ---
DB_URL = "postgresql://user:password@localhost:5433/crypto_db"
MODEL_PATH = "bitcoin_model.pkl"

st.set_page_config(page_title="Bitcoin Predictor", layout="wide")

# --- TITRE ---
st.title("💰 Real-Time Bitcoin Predictor")
st.markdown("Dashboard collecte data de **Kafka**, et stockée dans **Postgres**,  et faire une prediction avec **Machine Learning**.")

# --- FONCTIONS ---
def load_data():
    engine = create_engine(DB_URL)
    query = "SELECT timestamp, price_usd, ingestion_date FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, engine)
    return df.sort_values(by="timestamp") 

def load_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

# --- MAIN APP ---
try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error(f"Erreur: {e}")
    st.stop()

if not df.empty:
    # 2. Préparer les données pour Prediction
    last_row = df.iloc[-1]
    last_time = last_row['timestamp']
    last_price = last_row['price_usd']
    
    # Prédire le futur (+60 secondes)
    future_time = np.array([[last_time + 60]])
    predicted_price = model.predict(future_time)[0]
    
    # Calculer la différence
    diff = predicted_price - last_price
    color = "green" if diff > 0 else "red"
    direction = "HAUSSE 📈" if diff > 0 else "BAISSE 📉"

    # --- AFFICHAGE KPI (L-Ar9am l-kbars) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Prix Actuel (USD)", value=f"${last_price:,.2f}")
    
    with col2:
        st.metric(label="Prédiction (+1 min)", value=f"${predicted_price:,.2f}", delta=f"{diff:.2f}")
    
    with col3:
        st.markdown(f"### Tendance: :{color}[{direction}]")

    # --- GRAPHIQUE INTERACTIF (Plotly) ---
    st.subheader("Evolution du Prix")
    
    fig = go.Figure()
    
    # Courbe d Prix Reel
    fig.add_trace(go.Scatter(
        x=df['ingestion_date'], 
        y=df['price_usd'],
        mode='lines+markers',
        name='Prix Réel',
        line=dict(color='#1f77b4')
    ))
    
    # Point d Prediction
    future_date = pd.to_datetime(last_row['ingestion_date']) + pd.Timedelta(minutes=1)
    
    fig.add_trace(go.Scatter(
        x=[future_date],
        y=[predicted_price],
        mode='markers',
        name='Prediction AI',
        marker=dict(color='red', size=12, symbol='star')
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Bouton Refresh
    if st.button('🔄 Actualiser Data'):
        st.rerun()

else:
    st.warning("Mazal ma kayna data kafya f Database. Tsnna Consumer chwiya!")