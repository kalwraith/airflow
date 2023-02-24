# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum

with DAG(
    dag_id='dags_trigger_dagrun_operator',
    start_date=pendulum.datetime(2023,2,20),
    schedule=None,
    catchup=False
) as dag:

    start_task = BashOperator(
        task_id='start_task',
        bash_command='echo "start!"',
    )

    data_interal_end = '{{ data_interval_end }}'
    trigger_dag_task = TriggerDagRunOperator(
        task_id='trigger_dag_task',
        trigger_dag_id='dags_branch_decorator_example',
        execution_date=pendulum.parse(data_interal_end).add(days=-2),
        reset_dag_run=True
    )

    start_task >> trigger_dag_task