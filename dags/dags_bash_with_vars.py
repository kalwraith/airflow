# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
import pendulum

value = Variable.get('sample_key')

with DAG(
    dag_id='dags_bash_with_vars',
    start_date=pendulum.datetime(2023, 3, 1, tz='Asia/Seoul'),
    end_date=pendulum.datetime(2023, 6, 1, tz='Asia/Seoul'),
    catchup=True,
    schedule='0 1 * * *',
    default_args={
        'retries': 1
    }
) as dag:
    bash_bad_vars = BashOperator(
        task_id='bash_bad_vars',
        bash_command=f'echo "variable:{value}"'
    )

    bash_good_vars = BashOperator(
        task_id='bash_good_vars',
        bash_command='echo "{{var.value.sample_key}}"'
    )

    bash_bad_vars >> bash_good_vars