from operators.seoul_api_to_csv_operator import SeoulApiToCsvOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_seoul_api_corona',
    schedule='0 7 * * *',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    catchup=False
) as dag:
    seoul_api_task = SeoulApiToCsvOperator(
        task_id='seoul_api_task',
        http_conn_id='apikey_openapi_seoul_go_kr',
        dataset_nm='TbCorona19CountStatus',
        path='/opt/airflow/files/TbCorona19CountStatus/{{data_interval_end | ds_nodash }}',
        file_name='TbCorona19CountStatus.csv'
    )