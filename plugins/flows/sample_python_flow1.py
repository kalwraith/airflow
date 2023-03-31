from airflow.operators.python import PythonOperator
from operators.make_fin_operator import MakeFinOperator
from airflow.utils.task_group import TaskGroup
from common import get_task_group_id

def flow():
    task_meta = {
        'PROCESS_TYPE':'c',
        'SRC_TGT_SYSETM':'hc',
        'PROCESS_CODE':'',
        'TGT_LAYER':'l0',
        'TABLE_NAME':'tgt_table'
    }

    task_group_id = get_task_group_id(task_meta)
    with TaskGroup(group_id=task_group_id) as tg:
        def test():
            print('flow1 test')

        t1 = PythonOperator(
            task_id='sample_python_flow1',
            python_callable=test
        )

        fin_task = MakeFinOperator(
            task_meta=task_meta,
            path='l0/cm/table_name/##yyyy##/##MM##/##dd##',
            file_name='##yyyyMMdd|dd-1##.success'
        )

        fin_task2 = MakeFinOperator(
            task_id='direct_inserted_task_name_fin',
            path='l0/cm/table_name/##yyyy##/##MM##/##dd##',
            file_name='##yyyyMMdd##.success'
        )

        t1 >> fin_task >> fin_task2

    return tg