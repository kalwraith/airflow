from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pendulum
import random

with DAG(
    dag_id='dags_xcom_usage_with_bash',
    start_date=pendulum.datetime(2023,2,1,tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    fruit_list = ['Orange','Apple','Grape']
    selected_fruit = fruit_list[random.randint(0,2)]

    bash_task_1 = BashOperator(
        task_id='bash_task_1',
        bash_command="echo '{{ ti }}' && " 
                     f"/opt/airflow/plugins/shell/select_fruit.sh {selected_fruit} " +
                     f"{{{{ ti.xcom_push(key='Fruit_type', value='{selected_fruit}') }}}} "

    )

    bash_task_2 = BashOperator(
        task_id='bash_task_2',
        bash_command="echo return_value is: {{ ti.xcom_pull(task_ids='bash_task_1', key='return_value') }} && "
        "echo Value of Fruit_type is: {{ ti.xcom_pull(task_ids='bash_task_1', key='Fruit_type') }}"
    )

    bash_task_1 >> bash_task_2