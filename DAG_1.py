from datetime import datetime
import importlib
a1 = importlib.import_module("assignment-02-JG-0212.Module_1")
a3 = importlib.import_module("assignment-02-JG-0212.Module_3")
a4 = importlib.import_module("assignment-02-JG-0212.Module_4")

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator





with DAG(
    "ImageScraper",
    description="A DAG which scrapes top stories from GNews and stores unique values and related data in a PostGreSQL database",
    schedule="*/10 * * * *",
    start_date=datetime(2025, 2, 15),
    catchup=False,
    tags=["A2"],
) as dag:

    t1 = PythonOperator(
        task_id = "ts_scrape",
        python_callable = a1.top_stories_scrape,
        provide_context = True,
    )

    t2 = PythonOperator(
        task_id = "extract_thumbnails_headlines",
        python_callable = a3.extract_data,
        provide_context = True,
    )

    t3 = SQLExecuteQueryOperator(
        task_id="create_data_table",
        conn_id = 'a2_db',
        sql="""
            CREATE TABLE IF NOT EXISTS image_data (
            thumbnail BYTEA
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
        python_callable = a4.insert_data,
     )

    t1>>t2>>t3>>t5
