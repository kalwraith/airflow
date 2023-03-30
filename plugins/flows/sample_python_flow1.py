from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from operators.make_fin_operator import MakeFinOperator
import pendulum

def flow():

    def test():
        print('flow1 test')

    t1 = PythonOperator(
        task_id='sample_python_flow1',
        python_callable=test
    )

    fin_task = MakeFinOperator(
        task_id='sample_make_fin',
        path='l0/cm/{{params.flow1_table }}/##yyyy##/##MM##/##dd##',
        file_name='fin'
    )

    return t1 >> fin_task

