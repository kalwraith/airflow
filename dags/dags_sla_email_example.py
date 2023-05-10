from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
import pendulum
from airflow.models import Variable

email_str = Variable.get("email_target")
email_lst = email_str.split(',')

with DAG(
    dag_id='dags_sla_email_example',
    start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
    schedule='*/10 * * * *',
    catchup=False,
    default_args={
        'sla': timedelta(seconds=30),
        'email': email_lst
    }
) as dag:
    
    task_sleep_14 = BashOperator(
        task_id='task_sleep_14',
        bash_command='sleep 14'
    )
    
    task_sleep_13 = BashOperator(
        task_id='task_sleep_13',
        bash_command='sleep 13'
    )

    task_sleep_12 = BashOperator(
        task_id='task_sleep_12',
        bash_command='sleep 12',
        sla=timedelta(seconds=35)
    )

    task_sleep_11 = BashOperator(
        task_id='task_sleep_11',
        bash_command='sleep 11',
        sla=timedelta(seconds=35)
    )

    task_sleep_10 = BashOperator(
        task_id='task_sleep_10',
        bash_command='sleep 10',
    )

    task_sleep_9 = BashOperator(
        task_id='task_sleep_9',
        bash_command='sleep 9',
    )

    task_sleep_14 >> task_sleep_13 >> task_sleep_12 >> task_sleep_11 >> task_sleep_10 >> task_sleep_9
    
