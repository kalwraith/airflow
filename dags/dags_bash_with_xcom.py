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
        bash_command="echo XCOM_PUSHED {{ ti.xcom_push(key='bash_pushed',value='first_bash_message') }} && "
                     "echo $PUSHED_MSG"
    )

    bash_pull = BashOperator(
        task_id='bash_pull',
        env={'FIRST_VALUE': "{{ ti.xcom_push(key='bash_pushed') }}",
             'SECOND_VALUE': "{{ ti.xcom_push(key='return_value', task_ids='bash_push') }}"},
        bash_command="echo $FIRST_VALUE && echo $SECOND_VALUE "
    )
