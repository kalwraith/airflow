from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import pendulum


def flow():
    def test():
        print('sample python flow2')

    t2 = PythonOperator(
        task_id='sample_python_flow2',
        python_callable=test
    )

    return t2

