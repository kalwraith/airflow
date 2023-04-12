from airflow import DAG
import pendulum
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.decorators import task


with DAG(
    dag_id='dags_trigger_dag_run',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule='0 2 * * *',
    catchup=False
) as dag:

    @task(task_id='start_python')
    def start_python():
        print('start')

    trigger_task = TriggerDagRunOperator(
        task_id='trigger_task',
        trigger_dag_id='dags_python_with_conf',
        trigger_run_id=None,
        execution_date='{{data_interval_start - macros.dateutil.relativedelta.relativedelta(hours=-2)}}',
        reset_dag_run=True,
        wait_for_completion=False,
        poke_interval=60,
        allowed_states=['success'],
        failed_states=None
    )

    start_python() >> trigger_task
