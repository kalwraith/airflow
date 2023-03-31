from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from operators.make_fin_operator import MakeFinOperator
from airflow.decorators import task_group
import pendulum

@task_group(group_id='sample_task_group')
def flow():

    def test():
        print('flow1 test')

    t1 = PythonOperator(
        task_id='sample_python_flow1',
        python_callable=test
    )

    fin_task = MakeFinOperator(
        task_id='sample_make_fin',
        path='l0/cm/table_name/##yyyy##/##MM##/##dd##',
        file_name='##yyyyMMdd|dd-1##.success'
    )

    t1 >> fin_task

