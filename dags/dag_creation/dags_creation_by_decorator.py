from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag

# 데코레이터 방식
@dag(start_date=datetime(2023,2,20),
     schedule=None,
     catchup=False
     )
def generate_dag():
    empty_task = EmptyOperator(
        task_id='empty_task'
    )
dag = generate_dag()
