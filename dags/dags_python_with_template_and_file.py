from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id='dags_python_with_template_and_file',
    start_date=pendulum.datetime(2023,3,1, tz='Asia/Seoul'),
    schedule='0 1 * * *',
    catchup=False
) as dag:
    def run_sql(**kwargs):
        sql = kwargs['sql_file']
        with open(sql) as sql:
            print(sql)

    python_task1 = PythonOperator(
        task_id='python_task1',
        python_callable=run_sql,
        op_kwargs={'sql_file':'/opt/airflow/files/sqls/select_template.sql'},
        # templates_exts=['.sql']
    )

    python_task1