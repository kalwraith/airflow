from airflow import DAG
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_task_decorator',
    start_date=pendulum.datetime(2023,2,27, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    @task
    def python_function1():
        for i in range(0,5):
            print(i)

    task1 = python_function1()

    @task
    def python_function2():
        for i in range(10,15):
            print(i)

    task2 = python_function2()

    task1 >> task2
    