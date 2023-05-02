from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
import pandas as pd


class BigdataEnvKrApiToPostgresOperator(BaseOperator):

    def __init__(self, api_code, tgt_tbl_nm, option_dict: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = 'openapi_bigdata-environment.kr'
        self.postgres_conn_id = 'conn-db-postgres-custom'
        self.tgt_tbl_nm = tgt_tbl_nm
        self.endpoint = f'/user/openapi/api.call.do'
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
        start = 0
        total_row = '??'
        cnt = 0
        while True:
            self.log.info(f'start / total_row:{start} / {total_row}')
            row_df, total_row = self._call_api(self.base_url, start)
            self.log.info(f'추출 건수: {row_df.shape[0]}')
            total_row_df = pd.concat([total_row_df, row_df])
            if cnt == 30:
                break
            else:
                start += display
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

    def _call_api(self, base_url, start):
        import requests
        import json

        headers = {'Content-Type': 'application/json',
                   'charset': 'utf-8',
                   'Accept': '*/*'
                   }
        params = {'apiKey':self.api_code}
        request_url = f'{base_url}&start={start}&display=100'       # 100 고정 (max)
        self.log.info(f'request url:{request_url}')
        response = requests.post(request_url, headers=headers, params=params, verify=False)
        contents = json.loads(response.text)

        rslt = contents.get('data')
        row_df = pd.DataFrame(rslt)
        total_row = contents.get('total')

        return row_df, total_row