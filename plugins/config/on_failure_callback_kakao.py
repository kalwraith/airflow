from config.kakao_api import send_kakao_msg
from airflow.models import Variable
import pendulum

def on_failure_callback_to_kakao(context):
    client_id = Variable.get("kakao_client_secret")
    exception = context.get('exception') or 'exception 없음'
    ti = context.get('ti')
    dag_id = ti.dag_id
    task_id = ti.task_id
    data_interval_end = context.get('data_interval_end').in_timezone('Asia/Seoul')

    content = {f'{dag_id}.{task_id}': f'{exception}'}
    print(client_id)
    print(content)
    send_kakao_msg(client_id=client_id,
                   talk_title=f'task 실패 알람',
                   content=content)
