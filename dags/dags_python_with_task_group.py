from airflow import DAG
from airflow.decorators import task
from airflow.decorators import task_group
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(
    dag_id='dags_python_with_task_group',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False
) as dag:
    empty_start = EmptyOperator(task_id='empty_start')

    @task_group(group_id='first_group')
    def group_1():
        ''' 첫 번째 그룹에 대한 설명입니다. '''
        @task(task_id='inner_fuction1')
        def inner_func1(**kwargs):
            print('첫 번째 함수입니다.')

        def inner_func2():
            print('두 번째 함수입니다.')

        inner_function2 = PythonOperator(
            task_id='inner_function2',
            python_callable=inner_func2
        )

        inner_func1() >> inner_function2


    empty_final = EmptyOperator(task_id='empty_final')

    empty_start >> group_1()>> empty_final