from airflow import DAG
from datetime import datetime
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_bash_default_args',
    start_date=pendulum.datetime(2023,3,20, tz='Asia/Seoul'),
    schedule='2 0 * * *',
    catchup=False,
    default_args={
        'START_DATE':'ABC',
        'END_DATE':'EDF'
    }
) as dag:
    @task(task_id='python_task')
    def python_func(**kwargs):
        import pprint
        print(kwargs)

    python_func()