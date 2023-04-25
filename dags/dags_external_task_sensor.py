from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import PythonOperator
import pendulum
from datetime import timedelta
from airflow.utils.state import State

with DAG(
    dag_id='dags_external_task_sensor',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule='0 7 * * 1',
    catchup=False
) as dag:
    external_task_sensor = ExternalTaskSensor(
        task_id='external_task_sensor',
        external_dag_id='dags_branch_python_operator',
        external_task_id='task_b',
        allowed_states=[State.SKIPPED],
        execution_delta=timedelta(hours=-6)
    )