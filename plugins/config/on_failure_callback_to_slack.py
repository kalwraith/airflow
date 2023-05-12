from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook

def on_failure_callback_to_slack(context):
    ti = context.get('ti')
    dag_id = ti.dag_id
    task_id = ti.task_id
    err_msg = context.get('exception')
    #batch_date = context('data_interval_end').in_timezone('Asia/Seoul')

    slack_hook = SlackWebhookHook(slack_webhook_conn_id='conn_slack_airflow_bot')
    slack_hook.send(text=f'{dag_id}.{task_id} 실패 알람, 에러내용:{err_msg}')