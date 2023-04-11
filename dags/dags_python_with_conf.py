from airflow import DAG
from datetime import datetime
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_python_with_conf',
    start_date=pendulum.datetime(2023,3,20, tz='Asia/Seoul'),
    schedule='2 0 * * *',
    catchup=False,
    params={
        'ymd_1':'{{ (data_interval_end.in_timezone("Asia/Seoul") + macros.dateutil.relativedelta.relativedelta(days=-1)) | ds }}',
        'ymd_2':'{{ (data_interval_end.in_timezone("Asia/Seoul") + macros.dateutil.relativedelta.relativedelta(days=-2)) | ds }}',
        'ymd_3':'{{ (data_interval_end.in_timezone("Asia/Seoul") + macros.dateutil.relativedelta.relativedelta(days=-3)) | ds }}'
    }
) as dag:
    dag.doc_md = """\
    파이썬 오퍼레이터 params 테스트입니다. 
    """

    @task(task_id='task_sample')
    def task_sample(**kwargs):
        ymd_1 = kwargs['params']['ymd_1']
        print(ymd_1)

    task_sample()
