from dagster import IOManager, io_manager
import pandas as pd
import os

class CSVIOResource(IOManager):
    def __init__(self, base_dir):
        self._base_dir = base_dir

    def _get_path(self, context):
        return os.path.join(self._base_dir, context.asset_key.path[-1] + ".csv")

    def handle_output(self, context, obj):
        path = self._get_path(context)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if isinstance(obj, pd.DataFrame):
            obj.to_csv(path, index=False)
        else:
            raise Exception(f"Unsupported type for CSVResource: {type(obj)}")

    def load_input(self, path):
        path = self._get_path(path)
        return pd.read_csv(path)
    
@io_manager
def excel_io_manager(init_context):
    return CSVIOResource(base_dir=init_context.resource_config["base_dir"])