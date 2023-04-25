from airflow.sensors.bash import BashSensor
from airflow.operators.bash import BashOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_bash_sensor',
    start_date=pendulum.datetime(2023,3,1, tz='Asia/Seoul'),
    schedule='0 6 * * *',
    catchup=False
) as dag:

    sensor_task = BashSensor(
        task_id='sensor_task',
        env={'FILE':'/opt/airflow/files/tvCorona19VaccinestatNew/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/tvCorona19VaccinestatNew.csv'},
        bash_command=f'''echo $FILE && 
                        if [ -f $FILE ]; then 
                              exit 0
                        else 
                              exit 1
                        fi''',
        poke_interval=300,    # 5분
        timeout=60 * 60 * 24,  # 1일
        mode='poke',
        soft_fail=True
    )

    bash_task = BashOperator(
        task_id='bash_task',
        env={'FILE': '/opt/airflow/files/tvCorona19VaccinestatNew/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/tvCorona19VaccinestatNew.csv'},
        bash_command='echo "건수: `cat $FILE | wc -l`"'
    )

    sensor_task >> bash_task