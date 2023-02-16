# Package Import
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

dummy_dag = DAG(dag_id='dags_dummy_test',
          start_date=datetime(2023,2,16),
          schedule_interval='0 0 * * *')

t1 = DummyOperator(
    task_id='dummy_t1',
    dag=dummy_dag
)

t2 = DummyOperator(
    task_id='dummy_t2',
    dag=dummy_dag
)

t3 = DummyOperator(
    task_id='dummy_t3',
    dag=dummy_dag
)

t4 = DummyOperator(
    task_id='dummy_t4',
    dag=dummy_dag
)

t5 = DummyOperator(
    task_id='dummy_t5',
    dag=dummy_dag
)

t6 = DummyOperator(
    task_id='dummy_t6',
    dag=dummy_dag
)

t7 = DummyOperator(
    task_id='dummy_t7',
    dag=dummy_dag
)

t8 = DummyOperator(
    task_id='dummy_t8',
    dag=dummy_dag
)

[t1, t2] >> t3 >> t4 >> [t6, t7] >> t8
t5 >> t4