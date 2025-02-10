from datetime import datetime, timedelta
from Module_1 import top_stories_url
from Module_2 import top_stories_scrape
from Module_3 import extract_data
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

def pull_ts_url(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='top_stories_url', task_ids='base_scrape')
    return pulled_value_1

def pull_ts_scrape(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='top_stories_scrape', task_ids='top_stories_scrape')
    return pulled_value_1

from airflow.operators.python import PythonOperator

with DAG(
    "ImageScraper",

    # default_args={
    #     "depends_on_past": False,
    #     "email": ["airflow@example.com"],
    #     "email_on_failure": False,
    #     "email_on_retry": False,
    #     "retries": 1,
    #     "retry_delay": timedelta(minutes=5),
    # },
    description="A DAG which scrapes top stories from GNews and stores unique values and related data in a PostGreSQL database",
    schedule="0 * * * *",
    start_date=datetime(2025, 2, 10),
    catchup=False,
    tags=["A2"],
) as dag:

    t1 = PythonOperator(
        task_id = "base_scrape",
        python_callable = top_stories_url,
    )
    
    t2 = PythonOperator(
        task_id = "top_stories_scrape",
        python_callable = top_stories_scrape,
        op_args = [pull_ts_url],
    )
    
    t3 = PythonOperator(
        task_id = "extract_thumbnails_headlines",
        python_callable = top_stories_scrape,
        op_args = [pull_ts_url,pull_ts_scrape],
    )

    t4 = SQLExecuteQueryOperator(
        task_id="create_data_table",
        sql="""
            CREATE TABLE IF NOT EXISTS image_data (
            thumbnail TEXT
            );

            CREATE TABLE IF NOT EXISTS article_metadata (
            headline TEXT,
            article_date DATE,
            scrape_timestamp TIMESTAMP,
            PRIMARY KEY(headline,article_date)
            );

          """,
    )

    t5 = PythonOperator(
        task_id = "insert_entries",
        python_callable = top_stories_scrape,
        op_args = [pull_ts_url,pull_ts_scrape],
        provide_context  = True,
    )