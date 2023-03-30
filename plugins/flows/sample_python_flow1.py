from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from operators.make_fin_operator import MakeFinOperator
import pendulum

def flow():

    t1 = PythonOperator(
        task_id='sample_python_flow1',
        python_callable=test
    )

    fin_task = MakeFinOperator(
        task_id='sample_make_fin',
        path='l0/cm/{{params.flow1_table }}/{{ data_interval_end.in_timezone("Asia/Seoul").year }}/{{ data_interval_end.in_timezone("Asia/Seoul").month }}/{{ data_interval_end.in_timezone("Asia/Seoul").day }}',
        file_name='fin'
    )

    return t1 >> fin_task

