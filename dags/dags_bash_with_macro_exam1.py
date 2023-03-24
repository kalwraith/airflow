from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
import calendar

with DAG(
    dag_id='dags_bash_with_macro_exam1',
    start_date=pendulum.datetime(2023,3,1, tz='Asia/Seoul'),
    schedule='10 1 L * *',
    catchup=False
) as dag:

    exam_1 = BashOperator(
        task_id='exam_1',
        env={'START_DATE':'{{ (data_interval_start + macros.dateutil.relativedelta.relativedelta(days=9)) | ds }}',
             'END_DATE': '{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(days=9) + macros.dateutil.relativedelta.relativedelta(days=-1)) | ds }}',
             'END_TS': '{{ data_interval_end + macros.dateutil.relativedelta.relativedelta(days=9) }}'
        },
        bash_command='echo "START_DATE: $START_DATE" && '
                     'echo "END_DATE: $END_DATE" && '
                     'echo "END_TS: $END_TS" '

    )

    exam_1