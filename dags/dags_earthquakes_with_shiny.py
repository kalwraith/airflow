# Package Import
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

## Custom Import
from src_shiny.earthquakes import Earthquakes

earthquakes_dag = DAG(dag_id='dags_earthquakes_with_shiny',
          start_date=datetime(2023,2,12),
          schedule_interval='0 1 * * *')

earthquakes = Earthquakes()
t1 = PythonOperator(
    task_id='delete_earthquakes',
    python_callable=earthquakes.del_data,
    op_kwargs={'starttime': "{{ data_interval_start | ds }}", 'endtime': "{{ data_interval_end | ds }}"},
    dag=earthquakes_dag
)

t2 = PythonOperator(
    task_id='insert_earthquakes',
    python_callable=earthquakes.insrt_data,
    op_kwargs={'starttime': "{{ data_interval_start | ds }}", 'endtime': "{{ data_interval_end | ds }}"},
    dag=earthquakes_dag
)


t3 = BashOperator(
    task_id='log_task_result',
    bash_command=f'echo $HOSTNAME',
    dag=earthquakes_dag
)

t1 >> t2 >> t3