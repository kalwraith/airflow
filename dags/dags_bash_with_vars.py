# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

# plugins 폴더 공유를 통해 컨테이너 외부에 있는 shell 파일 수행하기
with DAG(
    dag_id='dags_bash_with_vars',
    start_date=pendulum.datetime(2023,3,1, tz='Asia/Seoul'),
    catchup=False,
    schedule='0 1 * * *'
) as dag:
    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo "{{var.value.sample}}"'
    )

    bash_task