from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
import pandas as pd


class WehagoApiToPostgresOperator(BaseOperator):

    def __init__(self, api_code, dataset_nm, tgt_tbl_nm, option_dict: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = 'datastore.wehago.com'
        self.postgres_conn_id = 'conn-db-postgres-custom'
        self.tgt_tbl_nm = tgt_tbl_nm
        self.endpoint = f'data/?dataset_key={dataset_nm}'
        self.api_code = api_code
        if option_dict:
            for k, v in option_dict.items():
                self.endpoint += f'&{k}={v}'

    def execute(self, context):
        import os
        from datetime import datetime
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from sqlalchemy import create_engine

        connection = BaseHook.get_connection(self.http_conn_id)
        self.base_url = f'https://{connection.host}/{self.endpoint}'

        total_row_df = pd.DataFrame()
        start_row = 0
        end_row = 499
        cnt = 0
        while True:
            self.log.info(f'start_row / end_row:{start_row} / {end_row}')
            row_df, row_size = self._call_api(self.base_url, start_row, end_row)
            self.log.info(f'추출 건수: {row_size}')
            total_row_df = pd.concat([total_row_df, row_df])
            if cnt == 30:
                break
            else:
                start_row = end_row + 1
                end_row += 500
            cnt += 1
            #import time
            #time.sleep(3)

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

    def _call_api(self, base_url, from_row, to_row):
        import requests
        import json

        headers = {'Content-Type': 'application/json',
                   'apicode': self.api_code,
                   'charset': 'utf-8',
                   'Accept': '*/*'
                   }

        request_url = f'{base_url}&from={from_row}&to={to_row}'
        self.log.info(f'request url:{request_url}')
        response = requests.get(request_url, headers=headers, verify=False)
        contents = json.loads(response.text)

        rslt = contents.get('data')
        row_df = pd.DataFrame(rslt)
        row_size = row_df.shape[0]

        return row_df, row_size