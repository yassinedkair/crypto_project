import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import os

# --- CONNECTION ---
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5433')
DB_URL = f"postgresql://user:password@{db_host}:{db_port}/crypto_db"

def train_advanced_model():
    print("🧠 Debut Training (Random Forest)...")
    
    try:
        engine = create_engine(DB_URL)
        
        query = "SELECT timestamp, price_usd FROM bitcoin_prices ORDER BY timestamp ASC"
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return

    if len(df) < 50:
        print("⚠️ Data est petit.")
        return

    # --- FEATURE ENGINEERING (SIRR DYAL MODEL) ---

    
    df['prev_price'] = df['price_usd'].shift(1) 
    df = df.dropna() 

    X = df[['prev_price']].values  # Feature 
    y = df['price_usd'].values     # Target 

    # --- TRAINING ---
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("✅ Model (Random Forest) trained.")

    # --- TEST PREDICTION ---
    last_real_price = df['price_usd'].iloc[-1]

    prediction = model.predict([[last_real_price]])[0]

    print("-" * 30)
    print(f"💰 Prix Actuel: {last_real_price:.2f}")
    print(f"🔮 Prediction: {prediction:.2f}")
    print("-" * 30)

    # --- SAVE ---
    save_path = 'scripts/bitcoin_model.pkl'
    
    with open(save_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"💾 Model saved to {save_path}")

if __name__ == "__main__":
    train_advanced_model()