from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook

class SeoulApiToCsvOperator(BaseOperator):
    template_fields = ('base_url', 'path','file_name')
    def __init__(self, http_conn_id, dataset_nm, path, file_name, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = http_conn_id
        self.path = path
        self.file_name = file_name
        self.base_url = '{{var.value.apikey_openapi_seoul_go_kr}}/json/' + dataset_nm

    def execute(self, context):
        import pandas as pd 
        import os
        import json
        
        connection = BaseHook.get_connection(self.http_conn_id)
        self.base_url = f'{connection.host}:{connection.port}/{self.base_url}'

        total_row_df = pd.DataFrame()
        start_row = 1
        end_row = 1000
        while True:
            self.log.info(f'시작:{start_row}')
            self.log.info(f'끝:{end_row}')
            row_df = self._call_api(self.base_url, start_row, end_row)
            total_row_df = pd.Concat(total_row_df, row_df)
            if len(row_df) < 1000:
                break
            else:
                start_row = end_row + 1
                end_row += 1000

        if not os.path.exists(self.path):
            os.system(f'mkdir -p {self.path}')
        total_row_df.to_csv(self.path + '/' + self.file_name, encoding='utf-8', index=False)

    def _call_api(self, base_url, start_row, end_row):
        import requests
        headers = {'Content-Type': 'application/json',
                   'charset': 'utf-8',
                   'Accept': '*/*'
                   }

        request_url = f'{base_url}/{start_row}/{end_row}/'
        response = requests.get(request_url, headers)
        contents = json.loads(response.text)

        key_nm = list(contents.keys())[0]
        row_data = contents.get(key_nm).get('row')
        row_df = df.DataFrame(row_data)

        return row_df