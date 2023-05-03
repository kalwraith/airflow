from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
import pendulum

with DAG(
    dag_id='dags_sla_email_example_1',
    start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
    schedule='*/30 * * * *',
    catchup=False,
    default_args={
        'sla': timedelta(minutes=5),
        'email': ['hjkim_sun@naver.com', 'kalwraith@gmail.com']
    }
) as dag:
    
    task1 = BashOperator(
        task_id='task1',
        bash_command='sleep 10m',
    )
    
    task2 = BashOperator(
        task_id='task2',
        bash_command='sleep 2m',
        sla=timedelta(minutes=1)
    )
    
