from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import pendulum

def flow():

    def test():
        print('sample python flow1')

    t1 = PythonOperator(
        task_id='sample_python_flow1',
        python_callable=test
    )

    return t1

