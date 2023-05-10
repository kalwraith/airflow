from config.kakao_api import send_kakao_msg
from airflow.models import Variable
def sla_miss_callback_to_kakao(dag, task_list, blocking_task_list, slas, blocking_tis):
    '''
    :param dag:
    :param task_list: delimiter(\n)로 구분된 list, (Ex: task_1 on 2023-05-10T006:00:00+00:00\ntask_2 on 2023-05-10T006:00:00+00:00)
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
    client_id = Variable.get("kakao_client_secret")
    #slas_lst = [i for i in slas[0]]

    content = {}
    content['1'] = type(slas)
    #content['3'] = slas_lst[4]
    # for task in task_list.split('\n'):
    #     content[task] = str(slas_lst[2])

    send_kakao_msg(client_id=client_id,
                   talk_title=f'{dag.dag_id} SLA Miss 발생',
                   content=content)
