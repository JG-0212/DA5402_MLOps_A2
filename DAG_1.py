from datetime import datetime, timedelta
from A2.Module_1 import m1
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
with DAG(
    "ImageScraper",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A DAG which scrapes top stories from GNews and stores unique values and related data in a PostGreSQL database",
    schedule="0 * * * *",
    start_date=datetime(2025, 2, 10),
    catchup=False,
    tags=["A2"],
) as dag:

    t1 = PythonOperator(
        task_id = "base_scrape",
        python_callable = m1,
    )