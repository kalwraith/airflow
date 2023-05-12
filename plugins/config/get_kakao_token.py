import requests
# client_id, authorize_code 노출 주의 

client_id='{client_id}'
redirect_uri = 'https://example.com/oauth'
authorize_code = '{authorize_code}}'


token_url = 'https://kauth.kakao.com/oauth/token'
data = {
    'grant_type':'authorization_code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(token_url, data=data)
tokens = response.json()
print(tokens)