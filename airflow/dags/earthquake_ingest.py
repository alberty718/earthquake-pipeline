from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
import psycopg2
import logging

logger = logging.getLogger(__name__)

sys.path.insert(0, '/opt/airflow/ingestion')
from fetch_earthquakes import fetch_events, insert_events

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def fetch_task():
    start_time = datetime.now() - timedelta(minutes=30)
    end_time = datetime.now()
    return fetch_events(start_time, end_time)

def validate_task(ti):
    events = ti.xcom_pull(task_ids='fetch_from_api')
    if not events:
        logger.info("No events in last 30 minutes, skipping")
        return []
    return events

def insert_task(ti):
    events = ti.xcom_pull(task_ids='validate_response')
    if not events:
        return 0
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=5432
    )
    try:
        cursor = conn.cursor()
        cnt = insert_events(events, cursor)
        conn.commit()
        return cnt
    finally:
        conn.close()


def log_task(ti):
    cnt = ti.xcom_pull(task_ids='upsert_to_raw')
    logger.info(f"Inserted {cnt} events into raw.earthquakes_raw")

with DAG(
    dag_id='earthquake_ingest',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval='*/15 * * * *',
    catchup=False
) as dag:
    
    t1 = PythonOperator(task_id='fetch_from_api', python_callable=fetch_task)
    t2 = PythonOperator(task_id='validate_response', python_callable=validate_task)
    t3 = PythonOperator(task_id='upsert_to_raw', python_callable=insert_task)
    t4 = PythonOperator(task_id='log_count', python_callable=log_task)

    t1 >> t2 >> t3 >> t4