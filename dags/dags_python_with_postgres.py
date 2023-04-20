from airflow import DAG
import pendulum
from airflow.decorators import task
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='dags_python_with_postgres',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    
    def insrt_postgres(ip, port, dbname, user, passwd, **kwargs):
        import psycopg2
        conn = psycopg2.connect(host=ip, dbname=dbname, user=user, password=passwd, port=int(port))
        cursor = conn.cursor()
        dag_id = kwargs.get('ti').get('dag_id')
        task_id = kwargs.get('ti').get('task_id')
        run_id = kwargs.get('ti').get('run_id')
        sql = 'insert into test_python_operator values (%s,%s,%s,%s);'
        msg = 'insrt 수행'
        cursor.execute(sql,(dag_id,task_id,run_id,msg))
        conn.commit()
        conn.close()
    
    insrt_postgres = PythonOperator(
        task_id='insrt_postgres',
        python_callable=insrt_postgres,
        op_args=['172.18.0.3', '5432', 'hjkim', 'hjkim', 'hjkim']
    )
        
    insrt_postgres
