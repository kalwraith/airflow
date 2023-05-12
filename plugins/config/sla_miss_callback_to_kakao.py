from config.kakao_api import send_kakao_msg
from airflow.models import Variable
import pendulum

def sla_miss_callback_to_kakao(dag, task_list, blocking_task_list, slas, blocking_tis):
    '''
    sla_miss_callback의 경우 print 하는 내용이 airflow Task Log에 남지 않으며 디버깅의 어려움이 존재함

    :param dag: DAG class 객체
    :param task_list: delimiter(\n)로 구분된 string, (Ex: task_1 on 2023-05-10T06:00:00+00:00\ntask_2 on 2023-05-10T006:00:00+00:00)
    :param blocking_task_list: Empty list
    :param slas: list로 감싸여진 slaMiss 객체
    :param blocking_tis: Empty list
    '''

    client_id = Variable.get("kakao_client_secret")
    content = {}
    for task in task_list.split('\n'):
        task_id = task.split(' ')[0]
        execution_date = task.split(' ')[2]
        execution_date_kr = pendulum.parse(execution_date, tz='UTC').in_timezone('Asia/Seoul').strftime('%Y-%m-%dT%H:%M:%S+09:00')
        content[task_id] = 'execution_date:' + execution_date_kr

    if len(content) == 1:           # content 길이는 2 이상
        content[''] = ''

    send_kakao_msg(client_id=client_id,
                   talk_title=f'{dag.dag_id} SLA Miss 발생',
                   content=content)
