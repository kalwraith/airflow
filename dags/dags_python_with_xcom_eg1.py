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
    @task(task_id='python_xcom_push_task')
    def xcom_push(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key="key1", value="value_1")
        ti.xcom_push(key="key2", value=[1, 2, 3])


    @task(task_id='python_xcom_pull_task')
    def xcom_pull(**kwargs):
        ti = kwargs['ti']
        value_key1 = ti.xcom_pull(key="key1")
        value_key2 = ti.xcom_pull(key="key2", task_ids='python_xcom_push_task')
        print(value_key1)
        print(value_key2)


    xcom_push() >> xcom_pull()

