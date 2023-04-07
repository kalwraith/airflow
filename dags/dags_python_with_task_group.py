from airflow import DAG
from airflow.decorators import task
from airflow.decorators import task_group
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
import pendulum

with DAG(
    dag_id='dags_python_with_task_group',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False
) as dag:
    def inner_func(**kwargs):
        msg = kwargs.get('msg') or ''
        print(msg)

    empty_start = EmptyOperator(task_id='empty_start')

    @task_group(group_id='first_group')
    def group_1():
        ''' task_group 데커레이터를 이용한 첫 번째 그룹입니다. '''

        @task(task_id='inner_fuction1')
        def inner_func1(**kwargs):
            print('첫 번째 함수입니다.')

        inner_function2 = PythonOperator(
            task_id='inner_function2',
            python_callable=inner_func,
            op_kwargs={'msg':'첫 번째 TaskGroup내 두 번쨰 task입니다.'}
        )

        inner_func1() >> inner_function2

    with TaskGroup(group_id='second_group') as group_2:
        @task(task_id='inner_fuction1')
        def inner_func3(**kwargs):
            print('세 번째 함수입니다.')


        inner_function2 = PythonOperator(
            task_id='inner_function2',
            python_callable=inner_func,
            op_kwargs={'msg': '두 번째 TaskGroup내 두 번쨰 task입니다.'}
        )

    empty_final = EmptyOperator(task_id='empty_final')

    empty_start >> [group_1(), group_2] >> empty_final