from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import pendulum
from flows import sample_python_flow1
from flows import sample_python_flow2

with DAG(
    dag_id='dags_python_unit_test',
    start_date=pendulum.datetime(2023,2,20, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False,
    params={
        'flow1_table':'TBL_TEST'
    }
) as dag:
    task_sample_python_flow1 = sample_python_flow1.flow()
    task_sample_python_flow2 = sample_python_flow2.flow()

    task_sample_python_flow1 >> task_sample_python_flow2