from operators.data_go_kr_api_to_postgres_operator import DataGoKrApiToPostgresOperator
from airflow import DAG
import pendulum

with DAG(
        dag_id='dags_datagokr_cancer',
        schedule=None,
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        catchup=False
) as dag:
    #유방암 환자수 현황
    patient_number = DataGoKrApiToPostgresOperator(
        task_id='real_unit_trtm_vo',
        dataset_group='B551172/brst',
        dataset_nm='patientNumber',
        tgt_tbl_nm='breast_cancer_patient_number'
    )


