from operators.seoul_api_to_postgres_operator import SeoulApiToPostgresOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_seoul_api_to_postgres',
    schedule='0 7 * * *',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    catchup=False
) as dag:
    tb_corona19_count_status = SeoulApiToPostgresOperator(
        task_id='tb_corona19_count_satus',
        dataset_nm='TbCorona19CountStatus',
        tgt_tbl_nm='TbCorona19CountStatus'
    ),
    
    tv_corona19_vaccine_stat_new = SeoulApiToPostgresOperator(
        task_id='tv_corona19_vaccine_stat_new',
        dataset_nm='tvCorona19VaccinestatNew',
        tgt_tbl_nm='tvCorona19VaccinestatNew'
    )

    tb_corona19_count_status >> tv_corona19_vaccine_stat_new