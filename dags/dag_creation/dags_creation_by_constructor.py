from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator

# 표준 생성자 방식
dag = DAG(
    dag_id='dags_creation_by_constructor',
    start_date=datetime(2023,2,20),
    schedule=None,
    catchup=False
)

empty_task = EmptyOperator(
    task_id='empty_task',
    dag=dag
)

empty_task