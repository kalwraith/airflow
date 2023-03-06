# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_bash_operator',
    start_date=pendulum.datetime(2023,2,16, tz='Asia/Seoul'),
    catchup=False,
    schedule='0 1 * * *'
) as dag:

    bash_task_1 = BashOperator(
        task_id='bash_task_1',
        bash_command='echo who_am_i',
    )

    bash_task_2 = BashOperator(
        task_id='bash_task_2',
        bash_command='echo $HOSTNAME',
    )

    bash_task_1 >> bash_task_2
