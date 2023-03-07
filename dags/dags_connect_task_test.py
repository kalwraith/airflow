# Package Import
from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(
    dag_id='dags_connect_task_test',
    start_date=pendulm.datetime(2023,2,16, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    t1 = EmptyOperator(
        task_id='t1',
    )

    t2 = EmptyOperator(
        task_id='t2',
    )

    t3 = EmptyOperator(
        task_id='t3',
    )

    t4 = EmptyOperator(
        task_id='t4',
    )

    t5 = EmptyOperator(
        task_id='t5',
    )

    t6 = EmptyOperator(
        task_id='t6',
    )

    t7 = EmptyOperator(
        task_id='t7',
    )

    t8 = EmptyOperator(
        task_id='t8',
    )

