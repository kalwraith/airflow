from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag

#1. with 방식
with DAG(
    dag_id='dags_creation_by_with_syntax',
    start_date=datetime(2023,2,20),
    schedule=None,
    catchup=False
) as dag:
    empty_task = EmptyOperator(
        task_id='empty_task'
    )

    empty_task

