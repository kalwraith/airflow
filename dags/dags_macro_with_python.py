from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id='dags_macro_with_python',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='10 1 * * 6#1',
    catchup=False
) as dag:

    def function_for_prev_month(start_date, end_date):
        print(f'기간 처리:{start_date} ~ {end_date}')

    task_1 = PythonOperator(
        task_id='task_1',
        templates_dict={'start_date':'{{ data_interval_end + macros.dateutil.relativedelta.relativedelta(months=-1, day=1) }}',
                        'end_date': '{{ data_interval_end - macros.dateutil.relativedelta.relativedelta(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1)}}'
                        },
        python_callable=function_for_prev_month
    )

    task_1