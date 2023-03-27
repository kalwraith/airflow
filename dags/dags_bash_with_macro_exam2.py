from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
import calendar

with DAG(
    dag_id='dags_bash_with_macro_exam2',
    start_date=pendulum.datetime(2023,3,1, tz='Asia/Seoul'),
    schedule='10 1 * * 6#2',
    catchup=False
) as dag:

    exam_2 = BashOperator(
        task_id='exam_2',
        env={'START_DATE':"{{ (data_interval_end.in_timezone('Asia/Seoul') + macros.dateutil.relativedelta.relativedelta(days=-19)) | ds }}",
             'END_DATE': "{{ (data_interval_end.in_timezone('Asia/Seoul') + macros.dateutil.relativedelta.relativedelta(days=-14)) | ds }}",
             'START_TS': "{{ data_interval_end.in_timezone('Asia/Seoul') + macros.dateutil.relativedelta.relativedelta(days=-1) }}"
        },
        bash_command='echo "START_DATE: $START_DATE" && '
                     'echo "END_DATE: $END_DATE" && '
                     'echo "START_TS: $START_TS"'

    )

    exam_2