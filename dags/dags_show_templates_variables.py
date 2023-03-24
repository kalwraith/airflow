# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
        dag_id='dags_show_templates_variables',
        start_date=pendulum.datetime(2023,2,16),
        schedule_interval='10 0 * * *',
        catchup=False) as dag:

    show_template_variables = BashOperator(
        task_id='show_template_variables',
        bash_command='\
            echo "data_interval_start | ds: {{ data_interval_start }}"; \
            echo "data_interval_end | ds: {{ data_interval_end }}"; \
            echo "dag_run.logical_date | ds: {{ dag_run.logical_date | ds }}"; \
            echo "dag_run.logical_date | ds_nodash: {{ dag_run.logical_date | ds_nodash }}"; \
            echo "dag_run.logical_date | ts: {{ dag_run.logical_date | ts }}"; \
            echo "ds: {{ ds }}"; \
            echo "ts: {{ ts }}"; \
            echo "ts_nodash_with_tz: {{ ts_nodash_with_tz }}"; \
            echo "ts_nodash: {{ ts_nodash }}"; \
            echo "prev_data_interval_start_success | ds: {{ prev_data_interval_start_success | ds }}"; \
            echo "prev_data_interval_end_success | ds: {{ prev_data_interval_end_success | ds }}"; \
            echo "prev_start_date_success | ds: {{ prev_start_date_success | ds }}"; '
    )

    show_template_variables