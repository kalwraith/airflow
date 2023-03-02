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
        env={'D_8':'{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-8)) | ds }}',
             'D_9':'{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-9)) | ds }}',
             'D_10': '{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-10)) | ds }}',
             'D_11': '{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-11)) | ds }}',
             'D_12': '{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-12)) | ds }}',
             'D_13': '{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=-13)) | ds }}'},
        bash_command='echo "d-8: $D_8" && '
                     'echo "d-9: $D_9" && '
                     'echo "d-10: $D_10" && '
                     'echo "d-11: $D_11" && '
                     'echo "d-12: $D_12" && '
                     'echo "d-13: $D_13" '

    )

    task_1