from airflow import DAG
from datetime import datetime
from airflow.decorators import task
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id='dags_bash_python_with_xcom',
    start_date=pendulum.datetime(2023,3,20, tz='Asia/Seoul'),
    schedule='2 0 * * *',
    catchup=False
) as dag:

    @task(task_id='python_result')
    def push_xcom():
        result_dict = {'status':'Good','data':[1,2,3],'options_cnt':100}
        return result_dict

    bash_pull = BashOperator(
        task_id='bask_pull',
        env={
            'STATUS':'{{ti.xcom_pull(task_ids="python_result")["status"]}}',
            'DATA':'{{ti.xcom_pull(task_ids="python_result")["data"]}}',
            'OPTIONS_CNT':'{{ti.xcom_pull(task_ids="python_result")["options_cnt"]}}'

        },
        bash_command='echo $STATUS && echo $DATA && echo $OPTIONS_CNT'
    )

    push_xcom() >> bash_pull