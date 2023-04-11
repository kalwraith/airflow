# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_simple_http_operator',
    start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
    catchup=False,
    schedule=None
) as dag:

    bash_task_1 = SimpleHttpOperator(
        task_id='bash_task_1',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='4c545370646b616c3733704a554a55/json/bikeListHist/1/10/2023041008',
        method='GET',
        headers={'Content-Type': 'application/json',
                        'charset': 'utf-8',
                        'Accept': '*/*'
                        }
    )
    
    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        from pprint import pprint
        pprint(ti.xcom_pull(task_ids='bash_task_1'))

    bash_task_1 >> python_2()