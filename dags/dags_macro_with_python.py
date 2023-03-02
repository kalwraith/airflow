from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id='dags_macro_with_python',
    start_date=pendulum.datetime(2023,2,1, tz='Asia/Seoul'),
    schedule='10 1 * * 6#1',
    catchup=False
) as dag:

    def function_for_prev_month(**kwargs):
        template_dict = kwargs.get('templates_dict') or {}
        if template_dict:
            start_date = template_dict.get('start_date') or 'start_date없음'
            end_date = template_dict.get('end_date') or 'end_date없음'
            print(f'기간 처리:{start_date} ~ {end_date}')
        else:
            print('templates_dict 파라미터가 없습니다')

    # 전월 1일 부터 말일까지 가져오기
    task_1 = PythonOperator(
        task_id='task_1',
        templates_dict={'start_date':'{{ data_interval_end + macros.dateutil.relativedelta.relativedelta(months=-1, day=1) }}',
                        'end_date': '{{ data_interval_end - macros.dateutil.relativedelta.relativedelta(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1)}}'
                        },
        python_callable=function_for_prev_month
    )

    task_1