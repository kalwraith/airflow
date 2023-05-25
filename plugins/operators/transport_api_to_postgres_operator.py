from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
import pandas as pd


class TransportApiToPostgresOperator(BaseOperator):
    template_fields = ('endpoint',)

    def __init__(self, product_id, tgt_tbl_nm, option_dict: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = 'openapi.transportation.kr'
        self.postgres_conn_id = 'conn-db-postgres-custom'
        self.tgt_tbl_nm = tgt_tbl_nm
        self.endpoint = 'api?apiKey={{var.value.apikey_openapi_transportation2}}&productId=' + product_id + '&numOfRows=1000'
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
        start_page = 1
        page_size = '??'
        while True:
            self.log.info(f'pageNo / pageSize:{start_page} / {page_size}')
            row_df, page_size = self._call_api(self.base_url, start_page)
            self.log.info(f'추출 건수: {row_df.shape[0]}')
            total_row_df = pd.concat([total_row_df, row_df])
            if int(page_size) <= start_page:
                break
            else:
                start_page = start_page + 1
            import time
            time.sleep(3)

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

    def _call_api(self, base_url, page_no):
        import requests
        import json

        headers = {'Content-Type': 'application/json',
                   'charset': 'utf-8',
                   'Accept': '*/*'
                   }

        request_url = f'{base_url}&pageNo={page_no}'
        self.log.info(f'request url:{request_url}')
        response = requests.get(request_url, headers=headers, verify=False)
        contents = json.loads(response.text)

        rslt = contents.get('result')
        for k, v in rslt.items():
            if k == 'pageSize':
                page_size = v
            if isinstance(v,list):
                row_df = pd.DataFrame(v)

        return row_df, page_size