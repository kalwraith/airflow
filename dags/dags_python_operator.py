from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator


def python_function1():
    sample_list = [1,2,3,4,5]
    return_lst = []
    for i in sample_list:
        return_lst.append(i)

    print(return_lst)


with DAG(
    dag_id='dags_python_operator',
    start_date=datetime(2023,2,20),
    schedule=None
) as dag:

    python_task_1 = PythonOperator(
        task_id='python_task_1',
        python_callable=python_function1
    )

    python_task_1
