from dagster import asset, Output, AssetIn
from src.utils.reports.download_reports import download_report, setup_driver, login
from src.utils.reports.config import REPORTS
from src.utils.data_cleaning import standardize_column_names
from src.ops.schedule_checker import run_schedule_checks
import pandas as pd

@asset(group_name="schedules")
def appointments_by_date():
    driver = setup_driver()
    login(driver)
    report = REPORTS['appointments_by_date']
    df = download_report(driver, report)
    standardized_df = standardize_column_names(df)
    return Output(standardized_df, metadata={"num_rows": len(standardized_df)})

@asset(group_name="schedules", ins={"appointments": AssetIn("appointments_by_date")})
def schedule_alerts(appointments):
    alerts_df = run_schedule_checks(appointments)
    return Output(alerts_df, metadata={"num_alerts": len(alerts_df)})

@asset(group_name="schedules", ins={"alerts": AssetIn("schedule_alerts")})
def schedule_alerts_report(alerts: pd.DataFrame):
    report = f"""
    Schedule Alerts Report
    ----------------------
    Total Alerts: {len(alerts)}

    Alert Types:
    {alerts['alert_type'].value_counts().to_string()}

    Top 5 Most Common Alerts:
    {alerts.head(5).to_string(index=False)}

    """
    return Output(report, metadata={"report_length": len(report)})
