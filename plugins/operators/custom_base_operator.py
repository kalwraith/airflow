from airflow.models.baseoperator import BaseOperator
from common import substitute_parameters_with_context

class CustomBaseOperator(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_meta = kwargs.get('task_meta') or {}
        self.task_id = 'sdf'


    def execute(self, context):
        '''
        로깅 등 공통로직 처리
        '''
        self.log.info(context)
        self.data_interval_end = context['data_interval_end']
        self._execute()


    def _execute(self):
        '''
        자식클래스에서 구현(execute 함수 대신 _execute 함수를 재정의 할 것 )
        '''
        pass

    def substitute_parameters(self, variable: str):
        return substitute_parameters_with_context(self.data_interval_end, self.dag_id, variable)


    def get_task_id(self, operator_name: str):
        process_type = self.task_meta.get('PROCESS_TYPE')
        process_code = self.task_meta.get('PROCESS_CODE')
        table_name = self.task_meta.get('TABLE_NAME')
        src_tgt_system = self.task_meta.get('SRC_TGT_SYSETM')
        tgt_layer = self.task_meta.get('TGT_LAYER')

        ## task_group_id 에 대한 네이밍 룰 셋팅
        self.task_id = f'task_{process_type}{src_tgt_system}_{process_code}{tgt_layer}_{table_name}_{operator_type}'
