from dagster import Definitions, load_assets_from_modules
from .assets import financials, schedules
from .jobs.analytics_job import analytics_job
from .jobs.schedule_checker_job import schedule_checker_job
from .resources.excel_resource import excel_io_manager
import os

all_assets = load_assets_from_modules([financials, schedules])

BASE_DIR = os.environ.get('OUTPUT_PATH', 'data')

defs = Definitions(
    assets=all_assets,
    jobs=[analytics_job, schedule_checker_job],
    resources={
        "io_manager": excel_io_manager.configured({"base_dir": BASE_DIR}),
    },
)
