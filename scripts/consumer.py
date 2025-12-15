import json
import psycopg2
from kafka import KafkaConsumer
from datetime import date

# --- CONFIGURATION ---
KAFKA_TOPIC = 'bitcoin-price'
KAFKA_SERVER = 'localhost:9092'

# DB Params
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "crypto_db"
DB_USER = "user"
DB_PASSWORD = "password"

def get_db_connection():
    try:
        return psycopg2.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return None

def create_table():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id SERIAL PRIMARY KEY,
                currency VARCHAR(50),
                price_usd FLOAT,
                timestamp BIGINT,
                ingestion_date TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

if __name__ == "__main__":
    create_table()
    print("📡 Consumer (Smart) demarer...")
    
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        for message in consumer:
            data = message.value
            
            # 1. Recuperer Data
            currency_val = data.get('crypto', data.get('currency'))
            price_val = data.get('price', data.get('price_usd'))
            ts_val = data.get('timestamp')
            
            # 2. Fixer le Problème de Date (Time vs DateTime)
            raw_date = data.get('time_str', data.get('ingestion_date'))
            
            
            if raw_date and len(str(raw_date)) <= 8:
                today_str = date.today().strftime("%Y-%m-%d")
                final_date = f"{today_str} {raw_date}"
            else:
                final_date = raw_date

            # 3. Insert f Database
            if currency_val and price_val:
                try:
                    sql = """
                    INSERT INTO bitcoin_prices (currency, price_usd, timestamp, ingestion_date)
                    VALUES (%s, %s, %s, %s);
                    """
                    cur.execute(sql, (currency_val, price_val, ts_val, final_date))
                    conn.commit()
                    print(f"💾 Sauvegardé: {price_val} USD ({final_date})")
                except Exception as e:
                    
                    print(f"⚠️ Erreur d'insertion: {e}")
                    conn.rollback()

    except KeyboardInterrupt:
        print("Arrete Consumer.")
    finally:
        if conn: conn.close()