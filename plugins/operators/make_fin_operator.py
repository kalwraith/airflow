from airflow.models.baseoperator import BaseOperator
from pathlib import Path

class MakeFinOperator(BaseOperator):
    template_fields = ['path', 'file_name']

    def __init(self, path, file_name, **kwargs):
        super().__init__(**kwargs)
        self.path = path[1:] if path.startswith('/') else path
        self.file_name = file_name

    def execute(self, context: Context):
        base_dir = '/opt/airflow/files/fin'
        tgt_dir = base_dir + '/' + self.path
        Path(tgt_dir).mkdir(parents=True, exist_ok=True)

        f = open(f'{base_dir}/{self.path}/{self.file_name}', 'w')
        f.close()
