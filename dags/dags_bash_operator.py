# Package Import
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG(dag_id='dags_bash_operator',
          start_date=datetime(2023,2,16),
          schedule_interval='0 1 * * *')

t1 = BashOperator(
    task_id='bash_task1',
    bash_command='/opt/airflow/plugins/shell/select_fruit.sh Orange',
    dag=dag
)

t1