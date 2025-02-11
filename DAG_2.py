import os
from datetime import datetime
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.email_operator import EmailOperator
from Module_6 import update_inserts
from airflow.decorators import task

def provide_path():
    parent = os.abspath(os.path.join(os.getcwd(),os.pardir))
    file_path = os.path.join(parent,r"run/status.txt")
    return file_path

def pull_inserts(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='return_value', task_ids='updater')
    return pulled_value_1


with DAG(
    "Mailer",

    # default_args={
    #     "depends_on_past": False,
    #     "email": ["airflow@example.com"],
    #     "email_on_failure": False,
    #     "email_on_retry": False,
    #     "retries": 1,
    #     "retry_delay": timedelta(minutes=5),
    # },
    description="A DAG which sends a mail whenever new entries are made",
    schedule="0 * * * *",
    start_date=datetime(2025, 2, 10),
    catchup=False,
    tags=["A2"],
) as dag:

    f1 = FileSensor(
        task_id='file_sensor_task',
        # fs_conn_id='my_file_system',
        filepath=provide_path(),
        poke_interval=3600,
    )

    f2 = PythonOperator(
        task_id = "updater",
        python_callable = update_inserts,
    )

    @task.branch(task_id="branch_task")
    def branch_func(ti=None):
        xcom_value = ti.xcom_pull(task_ids="updater")
        if xcom_value != 0:
            return "send_email"
        else:
            return None

    f3 = EmailOperator( 
        task_id='send_email', 
        to='me21b078@smail.iitm.ac.in', 
        subject='New rows added', 
    )