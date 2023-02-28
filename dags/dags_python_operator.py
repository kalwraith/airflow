from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator


def python_function1(*args):
    print(type(args))
    print(args)


def python_function2(**kwargs):
    name = kwargs.get('name') or ''
    address = kwargs.get('address') or ''
    age = kwargs.get('age') or ''
    print('name:' + name)
    print('address:' + address)
    print('age:' + age)

def python_function3(*args, **kwargs):
    print(args)
    print('ti:' + str(kwargs['ti']))
    print('dag_run:' + str(kwargs['dag_run']))


with DAG(
    dag_id='dags_python_operator',
    start_date=datetime(2023,2,20),
    schedule=None
) as dag:

    python_task_1 = PythonOperator(
        task_id='python_task_1',
        python_callable=python_function1,
        op_args=['We','are','studying','airflow']

    )

    python_task_2 = PythonOperator(
        task_id='python_task_2',
        python_callable=python_function2,
        op_kwargs={'name':'hjkim','address':'seoul'}
    )

    python_task_3 = PythonOperator(
        task_id='python_task_3',
        python_callable=python_function3,
        op_args=['python','operator'],
        op_kwargs={'name':'hjkim','address':'seoul'}
    )


    python_task_1 >> python_task_2 >> python_task_3