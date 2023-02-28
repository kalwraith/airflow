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

    @task
    def python_function1():
        tmp_lst = []
        for i in range(0,5):
            tmp_lst.append(i)
        return tmp_lst

    task1 = python_function1()

    @task(task_id='python_task_2')
    def python_function2(lst: list):
        return {'list_content':[i + 100 for i in lst]}


    @task
    def python_function3(dict_v):
        print(dict_v.get('list_content') or [])

    python_task_2 = python_function2(task1)
    task3 = python_function3(python_task_2)

    BashOperator(
        task_id='bash_task',
        bash_command="echo {{ ti.xcom_pull(task_ids='python_function2', key='return_value') }}"
    )
