from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id='dags_python_with_template',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False
) as dag:
    def python_function(end_date, **kwargs):
        print(kwargs)
        print(end_date)
        print('data_interval_end:' + str(kwargs['data_interval_end']))


    task_1 = PythonOperator(
        task_id='task_1',
        op_kwargs={'end_date':'{{ data_interval_end.in_timezone("Asia/Seoul") | ds}}' },
        python_callable=python_function
    )

    task_1