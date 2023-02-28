from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_template_with_bash',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        env={'NEXT_DT': '{{ data_interval_end }}'},
        bash_command='echo "We ran $NEXT_DT and task_instance is {{ ti }}"'
    )

    task_1