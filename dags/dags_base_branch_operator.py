# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.branch import BaseBranchOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

dag = DAG(dag_id='dags_base_branch_operator',
          start_date=datetime(2023,2,20),
          schedule_interval='*/5 * * * *',
          catchup=False
          )


class BaseBashOperator(BaseBranchOperator):
    def choose_branch(self, context):
        #context['ts'] 는 string 타입의 %Y-%m-%dT%H:%M:%S+00:00 을 반환함

        ts = datetime.strptime(context['ts'], '%Y-%m-%dT%H:%M:%S+00:00')
        if int(divmod(ts.minute,2)[1]) == 0:
            return 'bash_branch_task1'
        else:
            return 'empty_task_1'


bash_branch_task1 = BashOperator(
    task_id='bash_branch_task1',
    bash_command='/opt/airflow/plugins/shell/select_fruit.sh Orange',
    dag=dag
)

empty_task_1 = EmptyOperator(
    task_id='empty_task_1'
)

base_branch_operator = BaseBashOperator(
    task_id='base_branch_operator',
    dag=dag
)

base_branch_operator >> [bash_branch_task1, empty_task_1]