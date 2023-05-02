from operators.wehago_api_to_postgres_operator import WehagoApiToPostgresOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_datastore_api_to_postgres',
    schedule=None,
    start_date=pendulum.datetime(2023,5,1, tz='Asia/Seoul'),
    catchup=False
) as dag:
    # 네이버 수집 데이터
    wehago_api_to_postgres_task = WehagoApiToPostgresOperator(
        task_id='wehago_api_to_postgres_task',
        api_code='cea4bdaa-1479-4413-b5b4-1fd9f17c871b',
        dataset_nm='DATASET_WISENET_1',
        tgt_tbl_nm='naver_crawling'
    )
