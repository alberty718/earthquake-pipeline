FROM apache/airflow:2.9.1

RUN pip install dbt-core dbt-postgres

ENV DBT_LOG_PATH=/tmp/dbt_logs
ENV DBT_TARGET_PATH=/tmp/dbt_target