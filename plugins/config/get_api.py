import requests
import pprint
import json
import pandas as df
from datetime import datetime
# def get_api(key, start_row, end_row):
#     # url 입력
#     url = f'http://openapi.seoul.go.kr:8088/{key}/json/TbCorona19CountStatus/{start_row}/{end_row}'
#     url = 'https://www.bigdata-transportation.kr/api?apiKey=a12248c4-10b9-4b8d-bcfc-5e141b5bc091&productId=PRDTNUM_000000020313&numOfRows=100&sumTmUnitTypeCode=3&pageNo=1'
#
#     # url 불러오기
#     response = requests.get(url, verify=False)
#
#     #데이터 값 출력해보기
#     contents = json.loads(response.text)
#     from pprint import pprint
#     pprint(contents)
#     # key_nm = list(contents.keys())[0]
#     # row_data = contents.get(key_nm).get('row')
#     # last_dt = row_data[0].get('S_DT')
#     # last_date = last_dt[:10]
#     # last_date = last_date.replace('.','-').replace('/','-')
#     #
#     # #row_df = df.DataFrame(row_data)
#     # print(last_date)
#
#
# get_api('4c545370646b616c3733704a554a55',1001,1002)

### 1) 인가코드 받기 (url을 웹브라우저에서 직접 입력해야 함)
client_id='17ee2ef32122520198454553beeca638'
redirect_uri = 'https://example.com/oauth'
url = f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'


# 인가코드(23/05/09)
code = 'EsY3SUVuSVAfc5odalMxch7asy-bgvqlo6RRuiOkFdVTSE71E-M5oRikjP6hyclF6vMvEQo9c5sAAAGH_2bV3g'



### 2) 토큰 받기
token_url = 'https://kauth.kakao.com/oauth/token'
data = {
    'grant_type':'authorization_code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'code': code,
    }

# response = requests.post(token_url, data=data)
# tokens = response.json()
# print(tokens)

# 토큰(23/05/09)
access_token = 'J7HEmuoslPo3phBKvni4M8UcZH5V1hiVO-yMSw9UCj11WgAAAYf_Zv1M'
refresh_token = 'BokI4z-Sk2nfqKijg0diPF3y6khkACYgyB1Kls9hCj11WgAAAYf_Zv1K'



### 3) 톡 보내기
send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers = {
    "Authorization": f'Bearer {access_token}'
}

text_data = {
    'object_type': 'text',
    'text': '테스트입니다',
    'link': {
        'web_url': 'https://developers.kakao.com',
        'mobile_web_url': 'https://developers.kakao.com'
    },
    'button_title': '키워드'
}

list_data = {
    'object_type': 'list',
    'header_title': 'dag 수행결과',
    'header_link': {
        'web_url': 'http://www.daum.net',
        'mobile_web_url': 'http://m.daum.net',
        'android_execution_params': 'main',
        'ios_execution_params': 'main'
    },
    'contents':[
        {
            'title':'task1 수행 결과',
            'description': 'fail',
            'image_url': 'data:image/png;base64,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',
            'image_width':200,
            'image_height':40,
            'link':{
                'web_url': 'http://www.daum.net',
                'mobile_web_url': 'http://m.daum.net'
            }
        },
        {
            'title': 'task2 수행 결과',
            'description': 'success',
            'image_url': 'data:image/png;base64,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',
            'image_width': 200,
            'image_height': 40,
            'link': {
                'web_url': 'http://www.daum.net/contents/2',
                'mobile_web_url': 'http://m.daum.net/contents/2',
                'android_execution_params': '/contents/2',
                'ios_execution_params': '/contents/2'
            }
        }
    ],
    'buttons':[
        {
            'title':'웹으로 이동?',
            'link': {
                'web_url': 'http://www.daum.net/contents/1',
                'mobile_web_url': 'http://m.daum.net/contents/1'
            }

        },
        {
            'title': '웹으로 이동?',
            'link': {
                'web_url': 'http://www.daum.net/contents/2',
                'mobile_web_url': 'http://m.daum.net/contents/2'
            }
        }
    ]
}


data = {'template_object': json.dumps(list_data)}
response = requests.post(send_url, headers=headers, data=data)
print(response.status_code)