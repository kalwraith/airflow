# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from airflow.exceptions import AirflowException
import pendulum
from datetime import timedelta
from airflow.models import Variable

email_str = Variable.get("email_target")
email_lst = [email.strip() for email in email_str.split(',')]

with DAG(
    dag_id='dags_timeout_example_1',
    start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
    catchup=False,
    schedule=None,
    dagrun_timeout=timedelta(seconds=40),
    default_args={
        'execution_timeout': timedelta(seconds=20),
        'email_on_failure': True,
        'email': email_lst
    }
) as dag:
    bash_sleep_15 = BashOperator(
        task_id='bash_sleep_15',
        bash_command='sleep 15',
    )

    bash_sleep_14 = BashOperator(
        task_id='bash_sleep_14',
        bash_command='sleep 14',
    )

    bash_sleep_13 = BashOperator(
        task_id='bash_sleep_13',
        bash_command='sleep 13',
    )


    bash_sleep_15 >> bash_sleep_14 >> bash_sleep_13
    
    



