from airflow.hooks.base import BaseHook
import psycopg2
import pandas as pd
import sqlalchemy
import os

class CustomPostgresHook(BaseHook):

    def __init__(self, postgres_conn_id, **kwargs):
        self.postgres_conn_id = postgres_conn_id

    def get_conn(self):
        airflow_conn = BaseHook.get_connection(self.postgres_conn_id)
        self.host = airflow_conn.host
        self.user = airflow_conn.login
        self.password = airflow_conn.password
        self.dbname = airflow_conn.schema
        self.port = airflow_conn.port

        self.postgres_conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname, port=self.port)


    def bulk_load(self, table_name, file_name, delimiter: str, header_yn: bool):
        from sqlalchemy import create_engine
        
        self.get_conn()
        header = 0 if header_yn else None               # header_yn = True면 0, False면 None
        file_df = pd.read_csv(file_name, header=header, delimiter=delimiter)
        file_df = file_df.apply(lambda x: x.replace('\r',''))       # 개행문자 ^M 제거 
        uri = f'postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}'
        engine = create_engine(uri)
        file_df.to_sql(name=table_name,
                            con=engine,
                            schema='public',
                            if_exists='insert',
                            index=False
                        )
