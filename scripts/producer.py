import time
import json
import requests
from kafka import KafkaProducer
from datetime import datetime

# --- CONFIGURATION ---
TOPIC_NAME = 'bitcoin-price'

KAFKA_SERVER = 'localhost:9092' 

# --- 1. CONNEXION KAFKA ---
print(f"connexion Kafka f {KAFKA_SERVER}...")
try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    print("✅ Connexion réussie avec Kafka.")
except Exception as e:
    print(f"❌ erreur de connexion: {e}")
    exit()

# --- 2. FONCTION BACH TJIB DATA ---
def get_bitcoin_price():
    
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Nwajdo data zwina
            message = {
                'crypto': 'bitcoin',
                'price': data['bitcoin']['usd'],
                'timestamp': data['bitcoin']['last_updated_at'],
                'time_str': datetime.now().strftime("%H:%M:%S")
            }
            return message
        else:
            return None
    except:
        return None

# --- 3. BOUCLE  ---
if __name__ == "__main__":
    print("🚀 ingestion")
    
    while True:
        
        data = get_bitcoin_price()
        
        if data:
            
            producer.send(TOPIC_NAME, value=data)
            print(f"[{data['time_str']}] 💸 Bitcoin Price: {data['price']} USD -> Kafka")
        else:
            print("⚠️ je ne peux pas récupérer la data.")
            
        time.sleep(30)