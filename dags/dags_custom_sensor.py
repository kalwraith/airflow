from airflow.sensors.bash import BashSensor
from sensors.postgres_table_sensor import PostgresTableSensor
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_custom_sensor',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    postgres_table_sensor = PostgresTableSensor(
        task_id='postgres_table_sensor',
        table_name='tbcorona19countstatus',
        poke_interval=300,
        mode='reschedule'
    )