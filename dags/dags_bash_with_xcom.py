from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_bash_with_xcom',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    bash_push = BashOperator(
        task_id='bash_push',
        bash_command="echo START && "
                     "echo XCOM_PUSHED "
                     "{{ ti.xcom_push(key='bash_pushed',value='first_bash_message') }} && "
                     "echo COMPLETE"
    )

    bash_pull = BashOperator(
        task_id='bash_pull',
        bash_command="echo {{ ti.xcom_pull(key='bash_pushed') }} && echo {{ ti.xcom_pull(task_ids='bash_push') }} ",
        do_xcom_push=False
    )
