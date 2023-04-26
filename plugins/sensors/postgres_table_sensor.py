from airflow.sensors.base import BaseSensorOperator
from hooks.custom_postgres_hook import CustomPostgresHook

class PostgresTableSensor(BaseSensorOperator):
    template_fields = ('table_name')
    def __init__(self, postgres_conn_id, table_name, **kwargs):
        super().__init__(**kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table_name = table_name


    def poke(self, context):
        custom_postgres_hook = CustomPostgresHook(self.postgres_conn_id)
        postgres_conn = custom_postgres_hook.get_conn()
        cur = postgres_conn.cursor()
        check_sql = f"select count(1) from pg_tables where schemaname='public' AND tablename= %s ;"
        self.log.info(f'조회 쿼리: {check_sql}')

        cur.execute(check_sql, (self.table_name))
        rslt_set = cur.fetchall()
        rslt = int(rslt_set[0][0])
        self.log.info(f'테이블 개수: {rslt}')
        
        if rslt > 0:
            return True 
        else:
            return False