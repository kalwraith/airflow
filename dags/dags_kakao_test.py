from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from config.kakao_api import send_kakao_msg
import pendulum

with DAG(
    dag_id='dags_kakao_test',
    start_date=pendulum.datetime(2023,5,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    python_kakao_test = PythonOperator(
        task_id='python_kakao_test',
        python_callable=send_kakao_msg,
        op_kwargs={'talk_title':'dags_kakao_test수행결과','content':{
            'task A':'Success',
            'task B':'Failed'
        }}
    )

