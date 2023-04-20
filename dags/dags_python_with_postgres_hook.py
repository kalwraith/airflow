from airflow import DAG
import pendulum
from airflow.decorators import task
from airflow.operators.python import PythonOperator


with DAG(
        dag_id='dags_python_with_postgres_hook',
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        schedule=None,
        catchup=False
) as dag:
    def insrt_postgres(postgres_conn_id, **kwargs):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        postgres_hook = PostgresHook(postgres_conn_id)
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        dag_id = kwargs.get('ti').dag_id
        task_id = kwargs.get('ti').task_id
        run_id = kwargs.get('ti').run_id
        sql = 'insert into test_python_operator values (%s,%s,%s,%s);'
        msg = 'insrt 수행'
        cursor.execute(sql, (dag_id, task_id, run_id, msg))
        conn.commit()
        conn.close()

    insrt_postgres = PythonOperator(
        task_id='insrt_postgres',
        python_callable=insrt_postgres,
        op_kwargs={'postgres_conn_id':'conn-db-postgres-custom'}
    )