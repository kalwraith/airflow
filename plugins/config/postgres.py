import psycopg2

class Postgres():
    def __init__(self, dbname, user, passwd, host='127.0.0.1', port=5432):
        self.dbname = dbname
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.get_conn()

    def get_conn(self):
        self.conn = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user, password=self.passwd, port=self.port)
        self.cur = self.conn.cursor()



