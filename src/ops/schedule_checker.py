from dagster import op, Out
import pandas as pd
from datetime import datetime, timedelta
from src.utils.appointment_utils import (
    filter_appointments,
    check_time_gaps,
    check_appointment_types,
    check_appointment_notes,
    check_appointment_durations,
    check_medical_vs_cosmetic
)
from src.config.schedule_checker_config import (
    TIME_GAP_THRESHOLD,
    APPOINTMENT_TYPE_DURATIONS,
    COSMETIC_KEYWORDS
)

@op(out=Out(pd.DataFrame))
def run_schedule_checks(appointments_df: pd.DataFrame):
    # Filter appointments
    filtered_df = filter_appointments(appointments_df)
    
    # Run checks
    alerts = []
    alerts.extend(check_time_gaps(filtered_df, TIME_GAP_THRESHOLD))
    alerts.extend(check_appointment_types(filtered_df, APPOINTMENT_TYPE_DURATIONS))
    alerts.extend(check_appointment_notes(filtered_df))
    alerts.extend(check_appointment_durations(filtered_df, APPOINTMENT_TYPE_DURATIONS))
    alerts.extend(check_medical_vs_cosmetic(filtered_df, COSMETIC_KEYWORDS))
    
    # Create alerts DataFrame
    alerts_df = pd.DataFrame(alerts)
    
    # Log summary of alerts
    alert_summary = alerts_df['alert_type'].value_counts()
    print("Alert Summary:")
    print(alert_summary)
    
    return alerts_df
