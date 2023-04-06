# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.branch import BaseBranchOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id='dags_bash_python_with_xcom',
    start_date=pendulum.datetime(2023,3,20, tz='Asia/Seoul'),
    schedule='2 0 * * *',
    catchup=False
) as dag:
    def common_func(**kwargs):
        print(kwargs['selected'])


    class CustomBranchOperator(BaseBranchOperator):
        def choose_branch(self, context):
            import random

            item_lst = ['A', 'B', 'C']
            selected_item = random.choice(item_lst)
            if selected_item == 'A':
                return 'task_a'
            elif selected_item == 'B':
                return 'task_b'
            elif selected_item == 'C':
                return 'task_c'

    custom_branch_operator = CustomBranchOperator(task_id='branching')


    task_a = PythonOperator(
        task_id='task_a',
        python_callable=common_func,
        op_kwargs={'selected': 'A'}
    )

    task_b = PythonOperator(
        task_id='task_b',
        python_callable=common_func,
        op_kwargs={'selected': 'B'}
    )

    task_c = PythonOperator(
        task_id='task_c',
        python_callable=common_func,
        op_kwargs={'selected': 'C'}
    )

    custom_branch_operator >> [task_a, task_b, task_c]
