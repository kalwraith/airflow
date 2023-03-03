# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_bash_operator_plugins',
    start_date=datetime(2023,2,16),
    catchup=False,
    schedule='0 1 * * *'
) as dag:

    t1 = BashOperator(
        task_id='bash_task1',
        bash_command='echo who_am_i',
    )

    t2 = BashOperator(
        task_id='bash_task2',
        bash_command='echo $HOSTNAME',
    )

    t1 >> t2
    