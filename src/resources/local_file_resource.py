import os
import pandas as pd
from dagster import IOManager, resource
from string import Template

class LocalResource:
    def __init__(self, input_dir: str):
        self._input_dir = input_dir

    def load(self, filename: str, **kwargs) -> pd.DataFrame:
        input_path: str = os.path.join(self._input_dir, filename)
        if filename.endswith('.csv'):
            return pd.read_csv(input_path, **kwargs)
        elif filename.endswith('.parquet'):
            return pd.read_parquet(input_path, **kwargs)
        elif filename.endswith('.xlsx'):
            return pd.read_excel(input_path, **kwargs)


@resource
def local_file_resource(init_context) -> LocalResource:
    base_dir = init_context.resource_config.get("input_dir", os.path.join('data', 'input'))
    return LocalResource(base_dir)