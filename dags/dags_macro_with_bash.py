from airflow import DAG
from airflow.operators.bash import BashOperator

import pendulum

with DAG(
    dag_id='dags_macro_with_bash',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='10 1 * * 0#2',
    catchup=False
) as dag:

    # 2주 전 월요일부터 토요일까지 날짜 가져오기
    task_1 = BashOperator(
        task_id='task_1',
        env={'START_DATE':'{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-12)) | ds }}',
             'END_DATE': '{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-8)) | ds }}'},
        bash_command='echo "START_DATE: $START_DATE" && '
                     'echo "ENDDATE: $END_DATE" '

    )

    task_1