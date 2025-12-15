from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/opt/airflow/scripts')


from train_model_airflow import train_model

default_args = {
    'owner': 'yassine',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'crypto_retraining_pipeline',
    default_args=default_args,
    description='Automatisé Training dyal Bitcoin Model',
    schedule_interval=timedelta(minutes=10), 
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    training_task = PythonOperator(
        task_id='train_bitcoin_model',
        python_callable=train_model
    )