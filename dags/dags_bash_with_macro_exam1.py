from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_bash_with_macro_exam1',
    start_date=pendulum.datetime(2023,3,1, tz='Asia/Seoul'),
    schedule='10 1 * * *',
    catchup=False
) as dag:

    task_1 = BashOperator(
        task_id='task_1',
        env={'START_DATE':'{{ (data_interval_end.replace(day=1) - macros.dateutil.relativedelta.relativedelta(days=1)) | ds }}',
             'END_DATE': '{{ data_interval_start | ds }}'},
        bash_command='echo "START_DATE: $START_DATE" && '
                     'echo "ENDDATE: $END_DATE" '

    )

    task_1