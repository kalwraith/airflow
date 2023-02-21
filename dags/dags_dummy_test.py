# Package Import
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

empty_dag = DAG(dag_id='dags_connect_task_test',
          start_date=datetime(2023,2,16),
          schedule_interval=None,
          catchup=False)

t1 = EmptyOperator(
    task_id='dummy_t1',
    dag=empty_dag
)

t2 = EmptyOperator(
    task_id='dummy_t2',
    dag=empty_dag
)

t3 = EmptyOperator(
    task_id='dummy_t3',
    dag=empty_dag
)

t4 = EmptyOperator(
    task_id='dummy_t4',
    dag=empty_dag
)

t5 = EmptyOperator(
    task_id='dummy_t5',
    dag=dummy_dag
)

t6 = EmptyOperator(
    task_id='dummy_t6',
    dag=empty_dag
)

t7 = EmptyOperator(
    task_id='dummy_t7',
    dag=empty_dag
)

t8 = EmptyOperator(
    task_id='dummy_t8',
    dag=empty_dag
)

[t1, t2] >> t3 >> t4
t5 >> t4
[t6, t7] >> t8