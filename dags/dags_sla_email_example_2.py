from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
import pendulum

with DAG(
    dag_id='dags_sla_email_example_2',
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        schedule='*/40 * * * *',
        catchup=False
) as dag:
    
    task1 = BashOperator(
        task_id='task1',
        bash_command='sleep 10m',
        sla=timedelta(minutes=5), # SLA 설정
        email='hjkim_sun@naver.com'
    )
    
    task2 = BashOperator(
        task_id='task2',
        bash_command='sleep 2m',
        sla=timedelta(minutes=1), # SLA 설정
        email='hjkim_sun@naver.com'
    )
    
    task1 >> task2