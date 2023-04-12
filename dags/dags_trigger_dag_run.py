from airflow import DAG
import pendulum
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.decorators import task


with DAG(
    dag_id='dags_trigger_dag_run',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    @task(task_id='start_python')
    def start_python():
        print('start')

    trigger_task = TriggerDagRunOperator(
        task_id='trigger_task',
        trigger_dag_id='dags_python_with_conf'

    )

    start_python() >> trigger_task
