# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

# plugins 폴더 공유를 통해 컨테이너 외부에 있는 shell 파일 수행하기
with DAG(
    dag_id='dags_bash_operator_plugins',
    start_date=pendulum.datetime(2023,2,16, tz='Asia/Seoul'),
    catchup=False,
    schedule='0 1 * * *'
) as dag:

    t1 = BashOperator(
        task_id='bash_task1',
        bash_command='/opt/airflow/plugins/shell/select_fruit.sh Orange'
    )
    
    t1