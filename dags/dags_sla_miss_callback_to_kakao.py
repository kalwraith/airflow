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
    default_args={
        'sla': timedelta(seconds=20),
    },
    sla_miss_callback=sla_miss_callback_to_kakao
) as dag:
    task_sla_35s = BashOperator(
        task_id='task_sla_25s',
        bash_command='sleep 35',
    )

    task_sla_30s = BashOperator(
        task_id='task_sla_30s',
        bash_command='sleep 30',
    )

    task_sla_35s >> task_sla_30s

