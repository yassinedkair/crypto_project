
FROM apache/airflow:2.7.3

RUN pip install --no-cache-dir pandas scikit-learn sqlalchemy psycopg2-binary