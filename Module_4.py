import os
from datetime import datetime
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

class SQLConnectionError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

def pull_thumbnails_headlines(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='return_value', task_ids='extract_thumbnails_headlines')
    return pulled_value_1

def insert_1(data,**kwargs):
    print(type(data))
    sql_task = SQLExecuteQueryOperator(
        task_id="insert_image_data",
        conn_id='a2_db',
        sql="""
            INSERT INTO image_data (thumbnail)
            VALUES (%s);
            """,
        parameters = data,
    )
    return sql_task.execute(context=kwargs)

def insert_2(data,**kwargs):
    sql_task = SQLExecuteQueryOperator(
        task_id="insert_article_metadata",
        conn_id = 'a2_db',
        sql="""
            INSERT INTO article_metadata (headline,scrape_timestamp,article_date)
            VALUES (%s,%s,%s)
            ON CONFLICT(headline,article_date) DO NOTHING
            RETURNING 1;
            """,
        parameters = data,
    )
    result = sql_task.execute(context=kwargs)
    ti = kwargs['ti']
    ti.xcom_push(key = 'insert_entry', value = result)


def insert_data(**kwargs):

    thumbnails,headlines = pull_thumbnails_headlines(**kwargs)
    current_timestamp = datetime.now()
    article_date = current_timestamp.date().isoformat()

    id = 0
    for t,h in zip(thumbnails,headlines):
        insert_2((h,current_timestamp,article_date),**kwargs)
        ti = kwargs['ti']
        print(ti.xcom_pull(key='insert_entry'))
        if ti.xcom_pull(key = 'insert_entry')!=[[1]]:
            continue
        insert_1((t.encode('UTF-8'),),**kwargs)
        id += 1    
    run_dir = os.path.join(os.getcwd(), "dags/run")
    os.makedirs(run_dir, exist_ok=True)
    file_path = os.path.join(run_dir,"status.txt")
    with open(file_path, "w") as f:
        f.write(str(id))
    


