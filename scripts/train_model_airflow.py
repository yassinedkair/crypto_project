import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression

# Connexion DB (Port 5433)
DB_URL = "postgresql://user:password@postgres:5432/crypto_db"

def train_model():
    print("🧠 debut de Training...")
    
   
    try:
        engine = create_engine(DB_URL)
        query = "SELECT timestamp, price_usd FROM bitcoin_prices ORDER BY timestamp ASC"
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return

    
    if len(df) < 10:
        print(f"⚠️ Data small ({len(df)}). laisse consumer un peu de temps.")
        return
    
    print(f"📊 Dataset: {len(df)} lignes.")

   
    X = df[['timestamp']].values  # Features
    y = df['price_usd'].values    # Target

    # 4. Train
    model = LinearRegression()
    model.fit(X, y)
    print("✅ Model trained.")

    # 5. Predict Next Minute
    last_time = X[-1][0]
    future_time = np.array([[last_time + 60]])
    prediction = model.predict(future_time)[0]
    
    print("-" * 30)
    print(f"💰 prix Db: {y[-1]:.2f} USD")
    print(f"🔮 Prediction (+1m): {prediction:.2f} USD")
    print("-" * 30)

    # 6. Save Model
    with open('bitcoin_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("💾 Model 'bitcoin_model.pkl' sauvgardé.")

if __name__ == "__main__":
    train_model()