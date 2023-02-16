# Package Import
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG(dag_id='dags_show_templates_variables',
          start_date=datetime(2023,2,16),
          schedule_interval='0 1 * * *')

t1 = BashOperator(
    task_id='show_template_variables',
    bash_command='echo "dag_run.logical_date | ds: {{ dag_run.logical_date | ds }}"; \
     echo "dag_run.logical_date | ds_nodash: {{ dag_run.logical_date | ds_nodash }}"; \
     echo "dag_run.logical_date | ts: {{ dag_run.logical_date | ts }}"; \
     echo "prev_data_interval_start_success | ds: {{ prev_data_interval_start_success | ds }}"; \
     echo "prev_data_interval_end_success | ds: {{ prev_data_interval_end_success | ds }}"; \
     echo "prev_start_date_success | ds: {{ prev_start_date_success | ds }}"; \
     echo "dag: {{ dag }}"; \
     echo "task: {{ task }}"; \
     echo "macros: {{ macros }}"; \
     echo "task_instance: {{ task_instance }}";',
    dag=dag
)

t1