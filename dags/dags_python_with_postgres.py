from airflow import DAG
import pendulum
from airflow.decorators import task

with DAG(
    dag_id='dags_python_with_postgres',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:

    @task(task_id='insrt_postgres', op_args=['172.18.0.3','5432','hjkim','hjkim','hjkim'])
    def insrt_postgres(*args, **kwargs):
        import psycopg2
        conn = psycopg2.connect(host=args[0], dbname=args[2], user=args[3], password=args[4], port=int(args[1]))
        cursor = conn.cursor()
        dag_id = kwargs.get('dag_id')
        task_id = kwargs.get('task_id')
        run_id = kwargs.get('run_id')
        sql = 'insert into test_python_operator values (%s,%s,%s,%s);'
        msg = 'insrt 수행'
        cursor.execute(sql,(dag_id,task_id,run_id,msg))
        conn.commit()
        conn.close()
        
    insrt_postgres()
