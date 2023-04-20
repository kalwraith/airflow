from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
import pendulum
from dateutil.relativedelta import relativedelta

with DAG(
    dag_id='dags_file_sensor',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='0 7 * * *',
    catchup=False
) as dag:
    tvCorona19VaccinestatNew_sensor = FileSensor(
        task_id='tvCorona19VaccinestatNew_sensor',
        fs_conn_id='conn_file_opt_airflow_file',
        filepath='tvCorona19VaccinestatNew/{{data_interval_end | ds_nodash }}/tvCorona19VaccinestatNew.csv',
        recursive=False
    )

    TbCorona19CountStatus_sensor = FileSensor(
        task_id='file_sensor_task',
        fs_conn_id='conn_file_opt_airflow_file',
        filepath='/opt/airflow/files/TbCorona19CountStatus/{{data_interval_end | ds_nodash }}/TbCorona19CountStatus.csv',
        recursive=False
    )

    def count_corona_files(*args):
        import pandas as pd
        from pprint import pprint
        rslt_dict = {}

        for arg in args:
            file_name = arg.split('/')[-1]
            df = pd.read_csv(arg)
            rslt_dict[file_name] = len(df)
        
        
        pprint(rslt_dict)
    
    count_corona_files_task = PythonOperator(
        task_id='count_corona_files_task',
        python_callable=count_corona_files,
        op_args=['tvCorona19VaccinestatNew/{{data_interval_end | ds_nodash }}/tvCorona19VaccinestatNew.csv',
                 '/opt/airflow/files/TbCorona19CountStatus/{{data_interval_end | ds_nodash }}/TbCorona19CountStatus.csv']
    )


    [tvCorona19VaccinestatNew_sensor, TbCorona19CountStatus_sensor] >> count_corona_files_task