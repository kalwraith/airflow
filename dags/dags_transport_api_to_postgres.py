from operators.transport_api_to_postgres_operator import TransportApiToPostgresOperator
from airflow import DAG
import pendulum

with DAG(
        dag_id='dags_transport_api_to_postgres',
        schedule=None,
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        catchup=False
) as dag:
    #실시간 영업소간 통행시간
    real_unit_trtm_vo = TransportApiToPostgresOperator(
        task_id='real_unit_trtm_vo',
        product_id='PRDTNUM_000000020313',
        tgt_tbl_nm='real_unit_trtm_vo',
        option_dict={'sumTmUnitTypeCode:3'}
    )


