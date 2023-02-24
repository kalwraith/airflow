# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from datetime import datetime
import random

with DAG(dag_id='dags_branch_decorator_example',
          start_date=datetime(2023,2,16),
          schedule_interval='0 1 * * *',
        catchup=False
) as dag:

    @task.branch(task_id='branching')
    def random_branch():
        task_lst = ['task_a', 'task_b', 'task_c', 'task_d']
        select = random.randint(0, 3)
        return task_lst[select]

    branching = random_branch()

    task_a = BashOperator(
    task_id='task_a',
    bash_command='echo "Selected Task A!"'
    )

    task_b = BashOperator(
        task_id='task_b',
        bash_command='echo "Selected Task B!"'
    )

    task_c = BashOperator(
        task_id='task_c',
        bash_command='echo "Selected Task C!"'
    )

    task_d = BashOperator(
        task_id='task_d',
        bash_command='echo "Selected Task D!"'
    )

    branching >> [task_a,task_b,task_c,task_d]