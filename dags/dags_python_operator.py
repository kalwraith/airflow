from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator


def python_function(**kwargs):
    print(kwargs)



with DAG(
    dag_id='dags_python_operator',
    start_date=datetime(2023,2,20),
    schedule=None
) as dag:

    python_task_1 = PythonOperator(
        task_id='python_task_1',
        python_callable=python_function
    )

    python_task_1