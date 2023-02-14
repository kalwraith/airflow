from airflow.models import DAG
from airflow.operators.python import PythonOperator
from src_shiny.earthquakes import Earthquakes
from datetime import datetime

dag = DAG(dag_id='dags_earthquakes_with_shiny',
          start_date=datetime(2023,2,14),
          schedule_interval='0 1 * * *')

earthquakes = Earthquakes()
t1 = PythonOperator(
    task_id='delete_earthquakes',
    python_callable=earthquakes.del_data,
    op_kwargs={'starttime': "{{ prev_ds }}", 'endtime': "{{ next_ds }}"},
    dag=dag
)

t2 = PythonOperator(
    task_id='insert_earthquakes',
    python_callable=earthquakes.insrt_data,
    op_kwargs={'starttime': "{{ prev_ds }}", 'endtime': "{{ next_ds }}"},
    dag=dag
)

t1 >> t2