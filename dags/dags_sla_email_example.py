from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
import pendulum

with DAG(
    dag_id='dags_sla_email_example',
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        schedule='10 1 * * *',
        catchup=False
) as dag:
    
    task1 = BashOperator(
        task_id='task1',
        bash_command='sleep 10m',
        sla=timedelta(minutes=5), # SLA 설정
        email_on_failure=True, # 실패 시 이메일 전송 설정
        email_subject='SLA 미스', # 이메일 제목
        email_body='Task 1이 SLA를 미스하였습니다.', # 이메일 본문
    )
    
    task2 = BashOperator(
        task_id='task2',
        bash_command='sleep 2m',
        sla=timedelta(minutes=1), # SLA 설정
        email_on_failure=True, # 실패 시 이메일 전송 설정
        email_subject='SLA 미스', # 이메일 제목
        email_body='Task 2가 SLA를 미스하였습니다.', # 이메일 본문
    )
    
    task1 >> task2