from airflow.sensors.bash import BashSensor
from sensors.postgres_table_sensor import PostgresTableSensor
from sensors.seoul_api_today_sensor import SeoulApiTodaySensor
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
        postgres_conn_id='conn-db-postgres-custom',
        table_name='tbcorona19countstatus',
        poke_interval=300,
        mode='reschedule'
    )
    
    seoul_api_sensor = SeoulApiTodaySensor(
        task_id='seoul_api_sensor',
        dataset_nm='TbCorona19CountStatus',
        base_dt_col='S_DT',
        poke_interval=600,
        mode='reschedule'
    )