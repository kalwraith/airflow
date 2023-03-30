from airflow.models.baseoperator import BaseOperator
from common import substitute_parameters_with_context
class CustomBaseOperator(BaseOperator):
    from datetime import datetime
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_interval_end = kwargs['data_interval_end']

    def execute(self, context):




        self._execute()


    def _execute(self):
        '''
        자식클래스에서 구현(execute 함수 대신 _execute 함수를 재정의 할 것 )
        '''
        pass

    def substitute_parameters(self, variable: str):
        return substitute_parameters_with_context(data_inerval_end, variable)