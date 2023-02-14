from airflow.models import DAG
from airflow.operators.python import PythonOperator
from src_shiny.earthquakes import Earthquakes

dag = DAG(dag_id='dags_earthquakes_with_shiny',
          schedule_interval='0 1 * * *')

earthquakes = Earthquakes()
t1 = PythonOperator(
    task_id='delete earthquakes',
    python_callable=earthquakes.del_data,
    op_kwargs={'starttime': "{{ prev_ds }}", 'endtime': "{{ next_ds }}"},
    dags=dag
)

t2 = PythonOperator(
    task_id='insert earthquakes',
    python_callable=earthquakes.insrt_data,
    op_kwargs={'starttime': "{{ prev_ds }}", 'endtime': "{{ next_ds }}"},
    dag=dag
)

t1 >> t2