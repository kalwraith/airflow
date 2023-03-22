from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator


def python_function1(name, sex):
    print(f'name은 {name}이고 성별은 {sex}입니다')


with DAG(
    dag_id='dags_python_normal_variable',
    start_date=pendulum.datetime(2023,2,20, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    python_task_1 = PythonOperator(
        task_id='python_task_1',
        python_callable=python_function1,
        op_args=['hjkim','man']
    )

    python_task_2 = PythonOperator(
        task_id='python_task_2',
        python_callable=python_function1,
        op_kwargs={'name':'hjkim','sex':'man'}
    )

    python_task_1 >> python_task_2
