from dagster import define_asset_job
from src.assets.financials import payments_posted_by_date
from src.assets.schedules import appointments_by_date

analytics_job = define_asset_job(
    name="analytics_job",
    selection=[
        payments_posted_by_date.key,
        appointments_by_date.key,
    ],
)
