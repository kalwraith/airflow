from operators.custom_base_operator import CustomBaseOperator
from pathlib import Path
from common import get_task_id
class MakeFinOperator(CustomBaseOperator):
    template_fields = ('path','file_name')

    def __init__(self, path, file_name, **kwargs):
        task_meta = kwargs.get('task_meta') or ''
        if task_meta == '':
            task_id = kwargs.get('task_id')
        else:
            task_id = get_task_id(task_meta=task_meta, task_nm='make_fin')
        super().__init__(task_id=task_id, **kwargs)
        self.path = path[1:] if path.startswith('/') else path
        self.file_name = file_name


    def _execute(self):
        self.path = self.substitute_parameters(self.path)
        self.file_name = self.substitute_parameters(self.file_name)

        base_dir = '/opt/airflow/files/fin'
        tgt_dir = base_dir + '/' + self.path
        Path(tgt_dir).mkdir(parents=True, exist_ok=True)

        f = open(f'{base_dir}/{self.path}/{self.file_name}', 'w')
        f.close()
