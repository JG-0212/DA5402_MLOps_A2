import os
from datetime import datetime
import os
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

class WebDriverInitializationError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class BrowserAccessError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

class SQLConnectionError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass


def insert_1(data,**kwargs):
    sql_task = SQLExecuteQueryOperator(
        task_id="insert_image_data",
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
        sql="""
            INSERT INTO image_data (headline,scrape_timestamp,article_date)
            VALUES (%s,%s,%s)
            ON CONFLICT(headline,article_date) DO NOTHING
            RETURNING -1;
            """,
        parameters = data,
    )
    result = sql_task.execute(context=kwargs)
    ti = kwargs['ti']
    ti.xcom_push(key = 'insert_entry', value = result)


def insert_data(thumbnails,headlines,**kwargs):

    current_timestamp = datetime.now().isoformat()
    article_date = current_timestamp.date().isoformat()

    id = 0
    for t,h in zip(thumbnails,headlines):
        insert_2((h,current_timestamp,article_date),**kwargs)
        ti = kwargs['ti']
        if ti == -1:
            continue
        insert_1(t)
        id += 1
    
    parent = os.abspath(os.path.join(os.getcwd(),os.pardir))
    run_dir = os.path.join(parent, "run")
    os.makedirs(run_dir, exist_ok=True)
    file_path = os.path.join(run_dir,"status.txt")
    with open(file_path, "w") as f:
        f.write(id)
    



