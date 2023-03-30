from operators.make_fin_operator import MakeFinOperator
import pendulum
from airflow import DAG

with DAG(
    dag_id='dags_make_fin_test',
    start_date=pendulum.datetime(2023,3,20, tz='Asia/Seoul'),
    schedule='2 0 * * *',
    catchup=False,
) as dag:
    fin_task = MakeFinOperator(
        task_id='fin_task',
        path='l0/cm/{{ data_interval_end.in_timezone("Asia/Seoul").year }}/{{ data_interval_end.in_timezone("Asia/Seoul").month }}/{{ data_interval_end.in_timezone("Asia/Seoul").day }}',
        file_name='fin'
    )

    fin_task