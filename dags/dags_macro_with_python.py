from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
import pendulum
from dateutil.relativedelta import relativedelta

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
            print(f'기간 처리:{start_date} ~ {end_date} 작업을 시작합니다')
        else:
            print('templates_dict 파라미터가 없습니다')

    # 전월 1일 부터 말일까지 가져오기
    task_using_macros = PythonOperator(
        task_id='task_using_macros',
        templates_dict={'start_date':'{{ (data_interval_end + macros.dateutil.relativedelta.relativedelta(months=-1, day=1)) | ds }}',
                        'end_date': '{{ (data_interval_end - macros.dateutil.relativedelta.relativedelta(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1)) | ds }}'
                        },
        python_callable=function_for_prev_month
    )


    # 전월 1일부터 말일까지 python에서 직접 계산하기
    @task(task_id='task_direct_calc')
    def get_datetime_calc(**kwargs):
        data_interval_start = kwargs['data_interval_start']
        data_interval_end = kwargs['data_interval_end']
        data_interval_start = data_interval_start + relativedelta(months=-1, day=1)
        data_interval_end = data_interval_end + relativedelta(day=1) + relativedelta(days=-1)
        print('data_interval_start:' + str(data_interval_start))
        print('data_interval_end:' + str(data_interval_end))

        data_interval_start_str = data_interval_start.strftime('%Y-%m-%d')
        data_interval_end_str = data_interval_end.strftime('%Y-%m-%d')

        print('data_interval_start_str:' + data_interval_start_str)
        print('data_interval_end_str:' + data_interval_end_str)

    task_direct_calc = get_datetime_calc()

    task_using_macros >> task_direct_calc