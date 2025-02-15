import os
from datetime import datetime
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.email_operator import EmailOperator
import importlib
a6 = importlib.import_module('assignment-02-JG-0212.Module_6')
from airflow.decorators import task

def pull_inserts(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='return_value', task_ids='updater')
    return pulled_value_1

def status_deleter():
    os.remove('dags/run/status.txt')


with DAG(
    "Mailer",
    description="A DAG which sends a mail whenever new entries are made",
    schedule = "*/10 * * * *",
    start_date=datetime(2025, 2, 15),
    catchup=False,
    tags=["A2"],
) as dag:

    f1 = FileSensor(
        task_id='file_sensor_task',
        fs_conn_id='fs_default',
        filepath='dags/run/status.txt',
        poke_interval=60,
        timeout = 400,
        mode = 'reschedule',
    )

    f2 = PythonOperator(
        task_id = "updater",
        python_callable =a6.update_inserts,
        provide_context = True,
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
        subject='Alert: New rows added ',
        html_content = """<h3> New data alert </h3>
                       <p> {{ti.xcom_pull(task_ids = "updater")}} data points were added </p>""",
        ) 
    
    f4 = PythonOperator(
         task_id = 'deleter',
         python_callable = status_deleter,
        )
    f1>>f2>>f3>>f4
