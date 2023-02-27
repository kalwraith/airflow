# Package Import
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pendulum

## Custom Import
from src_shiny.earthquakes import Earthquakes

with DAG(dag_id='dags_earthquakes_with_shiny',
          start_date=pendulum.datetime(2023,2,12, tz='Asia/Seoul'),
          schedule_interval='0 1 * * *'
         ) as dag:

    earthquakes = Earthquakes()
    t1 = PythonOperator(
        task_id='delete_earthquakes',
        python_callable=earthquakes.del_data,
    )

    t2 = PythonOperator(
        task_id='insert_earthquakes',
        python_callable=earthquakes.insrt_data,
    )

    t3 = BashOperator(
        task_id='log_task_result',
        bash_command='echo "good nice" > /opt/airflow/plugins/{{ data_interval_end | ds }}.log',
    )

    t1 >> t2 >> t3