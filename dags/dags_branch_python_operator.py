from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
import random

def select_random():
    task_lst = ['task_a','task_b','task_c','task_d']
    select = random.randint(0,3)
    return task_lst[select]


def common_func(**context):
    params = context['params']
    print(params['selected'])

with DAG(
    dag_id='dags_branch_python_operator',
    start_date=datetime(2023,2,1),
    schedule=None,
    catchup=False
) as dag:

    start_task = BashOperator(
        task_id='start_task',
        bash_command='echo start!'
    )

    python_branch_task = BranchPythonOperator(
        task_id='python_branch_task',
        python_callable=select_random
    )

    task_a = PythonOperator(
        task_id='task_a',
        python_callable=common_func,
        params={'selected':'A'}
    )

    task_b = PythonOperator(
        task_id='task_b',
        python_callable=common_func,
        params={'selected':'B'}
    )

    task_c = PythonOperator(
        task_id='task_c',
        python_callable=common_func,
        params={'selected':'C'}
    )

    task_d = PythonOperator(
        task_id='task_d',
        python_callable=common_func,
        params={'selected':'D'}
    )

    start_task >> python_branch_task >> [task_a, task_b, task_c, task_d]