from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag

# 데코레이터 방식 (dag_id는 별도로 정의하지 않으며 함수명이 곧 dag_id가 된다)
@dag(start_date=datetime(2023,2,20),
     schedule=None,
     catchup=False
     )
def dags_creation_by_decorator():
    empty_task_1 = EmptyOperator(
        task_id='empty_task_1'
    )

    empty_task_2 = EmptyOperator(
        task_id='empty_task_2'
    )

    empty_task_1 >> empty_task_2

dag = dags_creation_by_decorator()
