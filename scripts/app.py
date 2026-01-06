import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from sqlalchemy import create_engine
import time

# --- 1. CONFIGURATION SIMPLE ---
st.set_page_config(page_title="Bitcoin AI", layout="wide", page_icon="🪙")

# Constants
MODEL_PATH = "scripts/bitcoin_model.pkl"
DB_URL = "postgresql://user:password@localhost:5433/crypto_db"

# CSS Custom 
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 30px;
    }
    .main {
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_resource
def load_resources():
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    except:
        return None

def get_data():
    try:
        engine = create_engine(DB_URL)
        query = "SELECT timestamp, price_usd, ingestion_date FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql(query, engine)
        df['ingestion_date'] = pd.to_datetime(df['ingestion_date'])
        return df.sort_values(by="timestamp").reset_index(drop=True)
    except:
        return pd.DataFrame()

# Fonction RSI (Simple)
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- 3. MAIN APP LOGIC ---
model = load_resources()
df = get_data()

if df.empty or model is None:
    st.info("⏳ Chargement des données... (Patientez)")
    time.sleep(2)
    st.rerun()

# Calculs
last_row = df.iloc[-1]
current_price = last_row['price_usd']
df['RSI'] = calculate_rsi(df['price_usd'])
current_rsi = df['RSI'].iloc[-1]

# Prediction (Random Forest uses Price input)
pred_input = np.array([[current_price]])
predicted_price = model.predict(pred_input)[0]

# Analyse
diff = predicted_price - current_price
trend = "HAUSSE ↗️" if diff > 0 else "BAISSE ↘️"
trend_color = "#00FF00" if diff > 0 else "#FF0000" # Green / Red

# --- 4. VISUALISATION (THE CLEAN PART) ---

# Titre
st.title("🪙 Bitcoin AI Tracker")

# A. LES CHIFFRES (KPIs)
k1, k2, k3, k4 = st.columns(4)

k1.metric(label="Prix Actuel", value=f"${current_price:,.2f}")
k2.metric(label="Prédiction (1 min)", value=f"${predicted_price:,.2f}", delta=f"{diff:.2f}")
k3.metric(label="RSI (Force)", value=f"{current_rsi:.1f}")
k4.markdown(f"""
    <div style="background-color: {trend_color}20; padding: 10px; border-radius: 5px; border: 1px solid {trend_color}; text-align: center;">
        <h3 style="color: {trend_color}; margin:0;">{trend}</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# B. LE GRAPHE PRINCIPAL (Clean & Simple)
fig = go.Figure()

# 1. Ligne du Prix (Bleu)
fig.add_trace(go.Scatter(
    x=df['ingestion_date'], 
    y=df['price_usd'],
    mode='lines',
    name='Prix Réel',
    line=dict(color='#29b5e8', width=3)
))

# 2. Point de Prédiction (Etoile Jaune)
future_time = pd.to_datetime(last_row['ingestion_date']) + pd.Timedelta(seconds=60)
fig.add_trace(go.Scatter(
    x=[future_time],
    y=[predicted_price],
    mode='markers+text',
    name='Cible AI',
    marker=dict(color='#ffd700', size=15, symbol='star'),
    text=[f"${predicted_price:.0f}"],
    textposition="top right"
))


fig.update_layout(
    title="Analyse du Prix en Temps Réel",
    template="plotly_dark",
    height=500,
    hovermode="x unified",
    xaxis=dict(showgrid=False, title="Temps"),
    yaxis=dict(showgrid=True, gridcolor='#333', title="Prix (USD)"),
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# C. GRAPHE SECONDAIRE (RSI - Juste une ligne)
st.caption("Indicateur RSI (Si la ligne est en bas = Bon moment pour acheter)")
fig_rsi = go.Figure()

fig_rsi.add_trace(go.Scatter(
    x=df['ingestion_date'],
    y=df['RSI'],
    mode='lines',
    name='RSI',
    line=dict(color='purple', width=2)
))


fig_rsi.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, line_width=0)
fig_rsi.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, line_width=0)

fig_rsi.update_layout(
    template="plotly_dark",
    height=200,
    margin=dict(l=0, r=0, t=10, b=0),
    yaxis=dict(range=[0, 100], showgrid=False)
)

st.plotly_chart(fig_rsi, use_container_width=True)

# Auto-Refresh 
time.sleep(2)
st.rerun()