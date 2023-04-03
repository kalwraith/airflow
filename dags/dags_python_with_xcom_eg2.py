from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_python_with_xcom_eg1',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False
) as dag:
    @task(task_id='xcom_push_by_return')
    def xcom_push_by_return(**kwargs):
        transaction_value = 'status Good'
        return transaction_value


    @task(task_id='xcom_pull_by_return')
    def xcom_pull_return_by_serial(status, **kwargs):
        print(status)


    @task(task_id='xcom_pull_by_return')
    def xcom_pull_return_by_method(**kwargs):
        ti = kwargs['ti']
        pull_value = ti.xcom_pull(key='return_value')
        print(pull_value)

    xcom_push = xcom_push_by_return()
    xcom_pull_by_return(xcom_push)
    xcom_push >> xcom_pull_return_by_method()