from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import psycopg2
import os

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def write_run_log(ti):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=5432
    )
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO monitoring.daily_run_log 
                (run_date, dag_id, dbt_status, finished_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                datetime.now().date(),
                'earthquake_daily_report',
                'success',
                datetime.now()
            )
        )
        conn.commit()
    finally:
        conn.close()

with DAG(
    dag_id='earthquake_daily_report',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    t1 = BashOperator(
        task_id='run_models',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir /opt/airflow/dbt'
    )

    t2 = PythonOperator(task_id='write_run_log', python_callable=write_run_log)

    t1 >> t2