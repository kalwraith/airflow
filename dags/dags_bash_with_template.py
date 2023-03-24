from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_template_with_bash',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    bash_t1 = BashOperator(
        task_id='bash_t1',
        bash_command='echo "End date is {{ data_interval_end }}"'
    )

    bash_t2 = BashOperator(
        task_id='bash_t2',
        env={'START_DATE': '{{ data_interval_start | ds}}','END_DATE':'{{ data_interval_end | ds }}'},
        bash_command='echo "Start date is $START_DATE " && '
                    'echo "End date is $END_DATE"'
    )


