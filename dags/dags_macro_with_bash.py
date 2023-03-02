from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_macro_with_bash',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='10 1 * * 0#1',
    catchup=False
) as dag:

    # 전월 마지막주 월요일부터 토요일까지 날짜 가져오기
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo "start_date: {{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(months=-1, weekday=MO(-1)) | ds) }}" && '
                     'echo "end_date: {{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(months=-1, weekday=SA(-1)) | ds ) }}" '

    )

    task_1