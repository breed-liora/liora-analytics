from dagster import IOManager, io_manager
import pandas as pd
import os

class ExcelIOManager(IOManager):
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def handle_output(self, context, obj):
        filename = f"{context.step_key}.xlsx"
        filepath = os.path.join(self.base_dir, filename)
        if isinstance(obj, pd.DataFrame):
            obj.to_excel(filepath, index=False)
        else:
            pd.DataFrame(obj.value).to_excel(filepath, index=False)
        context.log.info(f"Wrote dataframe to {filepath}")

    def load_input(self, context):
        filename = f"{context.upstream_output.step_key}.xlsx"
        filepath = os.path.join(self.base_dir, filename)
        return pd.read_excel(filepath)

@io_manager
def excel_io_manager(init_context):
    return ExcelIOManager(base_dir=init_context.resource_config["base_dir"])