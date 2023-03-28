from airflow import DAG
from datetime import datetime
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_python_with_conf',
    start_date=pendulum.datetime(2023,3,20, tz='Asia/Seoul'),
    schedule='2 0 * * *',
    catchup=False
) as dag:

    @task(task_id='task_sample')
    def task_sample(**kwargs):
        dag_run = kwargs['dag_run']
        print(dag_run.conf)

    task_sample()
