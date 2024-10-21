from dagster import define_asset_job
from src.assets.schedules import appointments_by_date, schedule_alerts, schedule_alerts_report

schedule_checker_job = define_asset_job(
    name="schedule_checker_job",
    selection=[
        appointments_by_date.key,
        schedule_alerts.key,
        schedule_alerts_report.key,
    ],
)
