from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_macro_with_bash',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo "You can calculate date: {{ data_interval_end + macros.dateutil.relativedelta.relativedelta(month=-1, day=1) }}"'
    )

    task_1