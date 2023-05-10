from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import json
import requests

CLIENT_ID = '17ee2ef32122520198454553beeca638'
REDIRECT_URL = 'https://example.com/oauth'
BASE_TOKEN_DIR = '/opt/airflow/plugins/config'
TOKENS_FILE = f'{BASE_TOKEN_DIR}/kakao_tokens.json'

def _refresh_token_to_json():
    with open(TOKENS_FILE, 'w') as token_file:
        tokens = json.load(token_file)
        refresh_token = tokens.get('refresh_token')
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": f"{CLIENT_ID}",
            "refresh_token": f"{refresh_token}"
        }
        response = requests.post(url, data=data)
        rslt = response.json()
        new_access_token = rslt.get('access_token')
        new_refresh_token = rslt.get('refresh_token')         # Refresh 토큰 만료기간이 30일 미만이면 refresh_token 값이 포함되어 리턴됨.
        if new_access_token:
            tokens['access_token'] = new_access_token
        if new_refresh_token:
            tokens['refresh_token'] = new_refresh_token

        json.dump(tokens, token_file)



def _is_access_token_expire():
    if not os.path.exists(TOKENS_FILE):
        return True

    else:
        access_issued_date = datetime.fromtimestamp(os.path.getmtime(TOKENS_FILE))
        print(f'발급일:{access_issued_date}')
        if relativedelta(datetime.now(), access_issued_date).hours > 6:
            return True
        else:
            return False


def send_kakao_msg(talk_title: str, content: dict):
    '''
    content:{'tltle1':'content1', 'title2':'content2'...}
    '''

    ### 1) 토큰 Expire 확인
    if _is_access_token_expire():
        _refresh_token_to_json()

    ### 2) get Access 토큰
    with open(TOKENS_FILE, 'r') as token_file:
        tokens = json.load(token_file)
        access_token = tokens.get('access_token')

    content_lst = []
    button_lst = []

    for title, msg in content.items():
        content_lst.append({
            'title': f'{title}',
            'description': f'{msg}',
            'image_url': '',
            'image_width': 40,
            'image_height': 40,
            'link': {
                'web_url': '',
                'mobile_web_url': ''
            }
        })
        button_lst.append({
            'title': '',
            'link': {
                'web_url': '',
                'mobile_web_url': ''
            }
        })

    list_data = {
        'object_type': 'list',
        'header_title': f'{talk_title}',
        'header_link': {
            'web_url': '',
            'mobile_web_url': '',
            'android_execution_params': 'main',
            'ios_execution_params': 'main'
        },
        'contents': content_lst,
        'buttons': button_lst
    }

    send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f'Bearer {access_token}'
    }
    data = {'template_object': json.dumps(list_data)}
    response = requests.post(send_url, headers=headers, data=data)
    print(f'reponse 상태:{response.status_code}')
    return response.status_code     #정상: 200 / 비정상: 401
