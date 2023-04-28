from airflow.sensors.base import BaseSensorOperator
from airflow.hooks.base import BaseHook

'''
서울시 공공데이터 API 추출시 특정 날짜 컬럼을 조사하여 
당일 날짜가 존재하는지 체크하는 센서 
1. 데이터셋에 날짜 컬럼이 존재하고
2. API 사용시 그 날짜 컬럼으로 ORDER BY DESC 되어 가져온다는 가정하에 사용 가능
'''

class SeoulApiTodaySensor(BaseSensorOperator):
    template_fields = ('endpoint')

    def __init__(self, dataset_nm, base_dt_col, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = 'openapi.seoul.go.kr'
        self.endpoint = '{{var.value.apikey_openapi_seoul_go_kr}}/json/' + dataset_nm + '/1/100'   # 100건만 추출
        self.base_dt_col = base_dt_col

    def poke(self, context):
        import requests
        import json
        connection = BaseHook.get_connection(self.http_conn_id)
        url = f'http://{connection.host}:{connection.port}/{self.endpoint}'
        self.log.info(f'request url:{url}')
        response = requests.get(url)

        contents = json.loads(response.text)
        key_nm = list(contents.keys())[0]
        row_data = contents.get(key_nm).get('row')
        last_dt = row_data[0].get(self.base_dt_col)
        last_date = last_dt[:10]
        last_date = last_date.replace('.', '-').replace('/', '-')
        try:
            pendulum.from_format(last_date, 'YYYY-MM-DD')
        except:
            from airflow.exceptions import AirflowException
            AirflowException(f'{base_dt_col} 컬럼은 YYYY.MM.DD 또는 YYYY/MM/DD 형태가 아닙니다.')

        today_ymd = kwargs.get('data_interval_end').in_timezone('Asia/Seoul').strftime('%Y-%m-%d')
        if last_date >= today_ymd:
            self.log.info(f'금일 데이터{today_ymd} 생성 확인')
            return True
        else:
            self.log.info(f'Update 미완료 (API Last 날짜:{last_date}, 금일 날짜: {today_ymd})')
            return False