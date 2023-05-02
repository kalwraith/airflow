from operators.bigdata_env_kr_api_to_postgres_operator import BigdataEnvKrApiToPostgresOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_bigdata_env_api_to_postgres',
    schedule=None,
    start_date=pendulum.datetime(2023,5,1, tz='Asia/Seoul'),
    catchup=False
) as dag:
    # 네이버 수집 데이터
    bigdata_env_kr_api_task = BigdataEnvKrApiToPostgresOperator(
        task_id='bigdata_env_kr_api_task',
        api_code='FF77B492AE3E48C898F5A39EA46FA36C',
        tgt_tbl_nm='food_trash_apartment'
    )
