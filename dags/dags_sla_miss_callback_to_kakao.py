from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
import pendulum
from config.sla_miss_callback_func import sla_miss_callback_to_kakao


with DAG(
    dag_id='dags_sla_miss_callback_to_kakao',
    start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
    schedule='*/10 * * * *',
    catchup=False,
    sla_miss_callback=sla_miss_callback_to_kakao
) as dag:
    task_sla_30s = BashOperator(
        task_id='task_sla_30s',
        bash_command='sleep 35',
        sla=timedelta(seconds=30)
    )

    task_sla_40s = BashOperator(
        task_id='task_sla_40s',
        bash_command='sleep 25',
        sla=timedelta(seconds=40)
    )

    task_sla_50s = BashOperator(
        task_id='task_sla_50s',
        bash_command='sleep 25',
        sla=timedelta(seconds=50)
    )

    task_sla_60s = BashOperator(
        task_id='task_sla_60s',
        bash_command='sleep 25',
        sla=timedelta(seconds=60)
    )



    task_sla_35s >> task_sla_30s >> task_sla_50s >> task_sla_10s

