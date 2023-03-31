from airflow.models.baseoperator import BaseOperator
from common import substitute_parameters_with_context
from airflow.utils.log.logging_mixin import LoggingMixin


class CustomBaseOperator(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pprint import pprint

        #self.data_interval_end = kwargs['data_interval_end']

    def execute(self, context):
        '''
        로깅 등 공통로직 처리
        '''
        LoggingMixin().log.info(self.dag_id)
        self.data_interval_end = context['data_interval_end']
        self._execute()


    def _execute(self):
        '''
        자식클래스에서 구현(execute 함수 대신 _execute 함수를 재정의 할 것 )
        '''
        pass

    def substitute_parameters(self, variable: str):
        from datetime import datetime
        return substitute_parameters_with_context(self.data_interval_end, self.dag_id, variable)