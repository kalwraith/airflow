from config.kakao_api import send_kakao_msg
from airflow.models import Variable
def sla_miss_callback_to_kakao(dag, task_list, blocking_task_list, slas, blocking_tis):
    '''
    :param dag:
    :param task_list:
    :param blocking_task_list:
    :param slas:
    :param blocking_tis:
    :return:
    '''
    print(
        "The callback arguments are: ",
        {
            "dag": dag,
            "task_list": task_list,
            "blocking_task_list": blocking_task_list,
            "slas": slas,
            "blocking_tis": blocking_tis,
        },
    )
    client_id=Variable.get("kakao_client_secret")
    #delay_task_instance = blocking_tis[0]
    #dag_id = delay_task_instance.dag_id

    content = {}
    for task in task_list.split('\n'):
        content[task] = f'sla Miss 발생'

    send_kakao_msg(client_id=client_id,
                   talk_title=f'dag SLA Miss 발생',
                   content=content)
