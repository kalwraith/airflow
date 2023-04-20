from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
import pandas as pd


class SeoulApiToPostgresOperator(BaseOperator):
    template_fields = ('endpoint', 'base_dt')

    def __init__(self, dataset_nm, tgt_tbl_nm, base_dt=None, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = 'openapi.seoul.go.kr'
        self.postgres_conn_id = 'conn-db-postgres-custom'
        self.tgt_tbl_nm = tgt_tbl_nm
        self.endpoint = '{{var.value.apikey_openapi_seoul_go_kr}}/json/' + dataset_nm
        self.base_dt = base_dt

    def execute(self, context):
        import os
        from datetime import datetime
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from sqlalchemy import create_engine
        
        connection = BaseHook.get_connection(self.http_conn_id)
        self.base_url = f'{connection.host}:{connection.port}/{self.endpoint}'

        total_row_df = pd.DataFrame()
        start_row = 1
        end_row = 1000
        while True:
            self.log.info(f'시작:{start_row}')
            self.log.info(f'끝:{end_row}')
            row_df = self._call_api(self.base_url, start_row, end_row)
            total_row_df = pd.concat([total_row_df, row_df])
            if len(row_df) < 1000:
                break
            else:
                start_row = end_row + 1
                end_row += 1000

        total_row_df.columns = [x.lower() for x in total_row_df.columns]
        total_row_df['load_dttm'] = datetime.now()
        total_row_df['load_dag_id'] = context['ti'].dag_id
        postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        postgres_uri = postgres_hook.get_uri()

        engine = create_engine(postgres_uri)
        total_row_df.to_sql(name=self.tgt_tbl_nm.lower(),
                  con=engine,
                  schema='public',
                  if_exists='replace',
                  index=False
                            )


    def _call_api(self, base_url, start_row, end_row):
        import requests
        import json

        headers = {'Content-Type': 'application/json',
                   'charset': 'utf-8',
                   'Accept': '*/*'
                   }

        request_url = f'{base_url}/{start_row}/{end_row}/'
        if self.base_dt is not None:
            request_url = f'{base_url}/{start_row}/{end_row}/{self.base_dt}'
        response = requests.get(request_url, headers)
        contents = json.loads(response.text)

        key_nm = list(contents.keys())[0]
        row_data = contents.get(key_nm).get('row')
        row_df = pd.DataFrame(row_data)

        return row_df