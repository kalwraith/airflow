import requests
import pandas as pd
import io
#from postgres import Postgres

from airflow.providers.postgres.hooks.postgres import PostgresHook
class Earthquakes():
    def _get_data(self, starttime, endtime):
        base_url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={starttime}&endtime={endtime}'
        headers = {'Content-Type': 'application/json',
                        'charset': 'utf-8',
                        'Accept': '*/*'
                        }
        resp = requests.get(base_url, headers=headers)
        with io.StringIO(resp.text) as f:
            csv_pd = pd.read_csv(f, encoding='utf-8', header=0)

        return csv_pd


    def _set_postgres_conn(self):
        self.hook = PostgresHook(postgres_conn_id='conn-postgres-custom')
        self.postgres_conn = self.hook.get_conn()
        #self.postgres_conn = Postgres(dbname='custom',user='hyunjinkim',passwd='hyunjinkim')


    def del_data(self, starttime, endtime):
        self._set_postgres_conn()
        self.postgres_conn.cur.execute(self._del_query(starttime, endtime))
        self.postgres_conn.conn.commit()


    def insrt_data(self, starttime, endtime):
        self._set_postgres_conn()
        earthquakes_pd = self._get_data(starttime, endtime)
        self.postgres_conn.cur.execute(self._insrt_query(earthquakes_pd))
        self.postgres_conn.conn.commit()


    def _del_query(self, starttime, endtime):
        return f'''DELETE FROM earthquakes WHERE TIME BETWEEN TO_TIMESTAMP('{starttime}','YYYY-MM-DD') AND TO_TIMESTAMP('{endtime}','YYYY-MM-DD')'''


    def _insrt_query(self, data_pd):
        values = ''
        for num, row in data_pd.iterrows():
            values += f"('{row['time']}',{row['depth']},{row['latitude']},{row['longitude']},{row['mag']}),\n"
        values = values[:-2]        # 끝 부분 콤마와 줄넘김 제거

        return f'''INSERT INTO earthquakes VALUES {values}'''
