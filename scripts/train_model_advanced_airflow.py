import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor 
import os

# --- CONFIGURATION ---
DB_URL = "postgresql://user:password@postgres:5432/crypto_db"

def train_model():
    print("🧠 Debut de Training (Mode: Random Forest Advanced)...")
    
    
    try:
        engine = create_engine(DB_URL)
        query = "SELECT timestamp, price_usd FROM bitcoin_prices ORDER BY timestamp ASC"
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return

    if len(df) < 50: 
        print(f"⚠️ Data est petit ({len(df)}). Attendre un peu.")
        return
    
    print(f"📊 Dataset: {len(df)} lignes chargé.")


    df['prev_price'] = df['price_usd'].shift(1)
    df = df.dropna() 

    X = df[['prev_price']].values  # Features 
    y = df['price_usd'].values     # Target

    # 3. Training
 
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("✅ Model (Random Forest) trained.")

    # 4. Test Prediction
    last_real_price = df['price_usd'].iloc[-1]
    prediction = model.predict([[last_real_price]])[0]
    
    print("-" * 30)
    print(f"💰 Prix Actuel: {last_real_price:.2f} USD")
    print(f"🔮 Prediction : {prediction:.2f} USD")
    print("-" * 30)

    # 5. Save Model
    save_path = 'scripts/bitcoin_model.pkl'
    try:
        with open(save_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"💾 Model '{save_path}' sauvgardé.")
    except Exception as e:

        print(f"⚠️ Probleme en save : {e}")
        # Fallback pour Docker (chemin absolu)
        with open('/opt/airflow/scripts/bitcoin_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        print("💾 Model sauvgardé (Chemin absolu Docker).")

if __name__ == "__main__":
    train_model()