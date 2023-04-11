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

    bike_list_hist = SimpleHttpOperator(
        task_id='bike_list_hist',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/json/bikeListHist/1/10/{{data_interval_end - macros.timedelta(}}',
        method='GET',
        headers={'Content-Type': 'application/json',
                        'charset': 'utf-8',
                        'Accept': '*/*'
                        }
    )

    vmsm_trdar_stor_qq = SimpleHttpOperator(
        task_id='vmsm_trdar_stor_qq',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/json/VwsmTrdarStorQq/1/10/2023',
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
        pprint(ti.xcom_pull(task_ids='bike_list_hist'))

    bike_list_hist >> python_2()
    vmsm_trdar_stor_qq