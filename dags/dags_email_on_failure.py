# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import timedelta
from airflow.models import Variable

email_str = Variable.get("email_target")
email_lst = email_str.split(',')

with DAG(
    dag_id='dags_email_on_failure',
    start_date=pendulum.datetime(2023,4,16, tz='Asia/Seoul'),
    catchup=False,
    schedule='0 1 * * *',
    dagrun_timeout=timedelta(minutes=2),
    default_args={
        'email_on_failure': True,
        'email': email_lst
    }
) as dag:
    task_sleep_180 = BashOperator(
        task_id='task_sleep_180',
        bash_command='sleep 180',
    )
    task_sleep_60 = BashOperator(
        task_id='task_sleep_60',
        bash_command='sleep 60',
    )



