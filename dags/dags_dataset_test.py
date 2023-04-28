from airflow import Dataset
from airflow import DAG
from airflow.operators.bash import BashOperator

sample_dataset = Dataset("produced_dag_dataset_test")

with DAG(
        dag_id='dag_dataset_test_produced',
        schedule='0 7 * * *',
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        catchup=False
) as dag1:
    bash_task_1 = BashOperator(
        task_id='bash_task_1',
        #outlets=[sample_dataset],
        bash_command='echo 1'
    )


with DAG(
        dag_id='dag_dataset_test_consumed',
        schedule=[sample_dataset],
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        catchup=False
) as dag2:
    bash_task_2 = BashOperator(
        task_id='bash_task_2',
        #outlets=[sample_dataset],
        bash_command='echo 1'
    )