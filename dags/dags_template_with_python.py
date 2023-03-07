from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id='dags_template_with_bash',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False
) as dag:

    @task(task_id='python_template')
    def python_function(**kwargs):
        print(kwargs)
        print('ds:' + kwargs['ds'])
        print('ts:' + str(kwargs['ts']))
        print('data_interval_start:' + kwargs['data_interval_start'])
        print('data_interval_end:' + kwargs['data_interval_end'])

    python_template = python_function()