import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

# --- CONFIG ---
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5433')
DB_URL = f"postgresql://user:password@{db_host}:{db_port}/crypto_db"
MODEL_PATH = "scripts/bitcoin_model.pkl" 

def evaluate():
    print("📊 Evaluation du Model en cours...")
    
    # 1. Load Model & Data
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        engine = create_engine(DB_URL)
        df = pd.read_sql("SELECT price_usd FROM bitcoin_prices ORDER BY timestamp ASC", engine)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    if len(df) < 100:
        print("⚠️ Pas assez de données pour évaluer (Mzyan tkoun +100 lignes).")
        return

    # 2. Préparer Test Data 
    df['Actual_Price'] = df['price_usd']
    df['Prev_Price'] = df['price_usd'].shift(1) # Feature
    df = df.dropna()

    X = df[['Prev_Price']].values
    y_true = df['Actual_Price'].values

    # 3. Faire des Predictions
    y_pred = model.predict(X)

    # --- CALCUL DES METRICS ---

    # A. Erreur b Dollars
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    # B. Direction (Trend) Accuracy
    actual_direction = df['Actual_Price'] > df['Prev_Price']
    predicted_direction = y_pred > df['Prev_Price'].values
    
   
    accuracy = np.mean(actual_direction == predicted_direction) * 100

    # --- RAPPORT ---
    print("\n" + "="*40)
    print("      📝 RESULTATS DU TEST (REPORT CARD)")
    print("="*40)
    print(f"🔹 Nombre de tests : {len(df)} lignes")
    print("-" * 40)
    print(f"💵 MAE (Moyenne Erreur) : ${mae:.2f}")
    print(f"   (le model fait des erreur de ${mae:.0f})")
    print("-" * 40)
    print(f"📈 Direction Accuracy   : {accuracy:.2f}%")
    
    if accuracy > 55:
        print("   ✅ Conclusion: MODEL PROFITABLE!")
    elif accuracy > 50:
        print("   ⚠️ Conclusion: Model normal (Coin Flip).")
    else:
        print("   ❌ Conclusion: Model mauvaise (Don't trade).")
    print("="*40 + "\n")

if __name__ == "__main__":
    evaluate()