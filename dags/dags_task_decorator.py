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
        tmp_lst = []
        for i in range(0,5):
            tmp_lst.append(i)
        return tmp_lst

    task1 = python_function1()

    @task
    def python_function2(lst: list):
        for x in lst:
            print(x)

    task2 = python_function2(task1)

    task2
