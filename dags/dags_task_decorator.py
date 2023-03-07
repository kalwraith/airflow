from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_task_decorator',
    start_date=pendulum.datetime(2023,2,27, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    @task(task_id='py_task_1')
    def python_function1():
        tmp_lst = []
        for i in range(0,5):
            tmp_lst.append(i)
        return tmp_lst

    py_task_1 = python_function1()

    @task(task_id='py_task_2')
    def python_function2(lst: list):
        return {'list_content':[i + 100 for i in lst]}


    py_task_2 = python_function2(py_task_1)




