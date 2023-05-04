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
        dag_id='dags_execution_timeout',
        start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
        catchup=False,
        schedule='0 1 * * *',
        dagrun_timeout=timedelta(minutes=2),
        default_args={
            'execution_timeout': timedelta(minutes=1),
            'email_on_failure': True,
            'email': email_lst
        }
) as dag:

    bash_sleep_2m = BashOperator(
        task_id='bash_sleep_2m',
        bash_command='sleep 2m',
    )
    
    bash_sleep_30 = BashOperator(
        task_id='bash_sleep_30',
        bash_command='sleep 30',
    )


