# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_email_on_failure',
    start_date=pendulum.datetime(2023,2,16, tz='Asia/Seoul'),
    catchup=False,
    schedule='0 1 * * *',
    default_args={
        'email_on_failure': True,
        'email': 'hjkim_sun@naver.com'
    }
) as dag:
    bash_task_1 = BashOperator(
        task_id='bash_task_1',
        bash_command='exit 1',
    )
    bash_task_2 = BashOperator(
        task_id='bash_task_2',
        bash_command='exit 0',
    )



