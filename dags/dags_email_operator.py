from airflow import DAG
from pendulum import datetime
from airflow.operators.email import EmailOperator

with DAG(
    dag_id='dags_email_operator',
    start_date=pendulum.datetime(2023,2,16, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    email_t1 = EmailOperator(
        task_id='email_t1',
        to='hjkim_sun@naver.com',
        subject='Airflow Test 메일입니다',
        html_content="""
                    이 메일은 테스트 메일입니다.<br/><br/>

                    {{ ds }}<br/>
                """
    )

    email_t1
