import pandas as pd
from datetime import datetime, timedelta

def filter_appointments(df: pd.DataFrame) -> pd.DataFrame:
    today = datetime.now().date()
    one_month_from_now = today + timedelta(days=30)
    
    return df[
        (df['appointment_date'] > today) &
        (df['appointment_date'] <= one_month_from_now)
    ]

def check_time_gaps(df: pd.DataFrame, threshold: timedelta) -> list:
    alerts = []
    sorted_df = df.sort_values(['appointment_date', 'appointment_time'])
    
    for i in range(1, len(sorted_df)):
        prev_appt = sorted_df.iloc[i-1]
        curr_appt = sorted_df.iloc[i]
        
        time_diff = datetime.combine(curr_appt['appointment_date'], curr_appt['appointment_time']) - \
                    datetime.combine(prev_appt['appointment_date'], prev_appt['appointment_time'])
        
        if time_diff > threshold:
            alerts.append({
                'alert_type': 'Large Time Gap',
                'patient_mrn': curr_appt['patient_mrn'],
                'appointment_date': curr_appt['appointment_date'],
                'appointment_time': curr_appt['appointment_time'],
                'appointment_duration': curr_appt['appointment_duration'],
                'rationale': f'Large gap of {time_diff} between appointments',
                'recommended_action': 'Consider scheduling appointments in this gap',
                'additional_info': f'Previous appointment ended at {prev_appt["appointment_time"]}'
            })
    
    return alerts

def check_appointment_types(df: pd.DataFrame, type_durations: dict) -> list:
    alerts = []
    
    for _, appt in df.iterrows():
        if appt['appointment_type'] in type_durations:
            expected_duration = type_durations[appt['appointment_type']]
            if appt['appointment_duration'] != expected_duration:
                alerts.append({
                    'alert_type': 'Incorrect Appointment Type',
                    'patient_mrn': appt['patient_mrn'],
                    'appointment_date': appt['appointment_date'],
                    'appointment_time': appt['appointment_time'],
                    'appointment_duration': appt['appointment_duration'],
                    'rationale': f'Duration does not match expected for {appt["appointment_type"]}',
                    'recommended_action': 'Review and adjust appointment type or duration',
                    'additional_info': f'Expected duration: {expected_duration} minutes'
                })
    
    return alerts

def check_appointment_notes(df: pd.DataFrame) -> list:
    alerts = []
    important_keywords = ['urgent', 'ASAP', 'emergency', 'follow-up required']
    
    for _, appt in df.iterrows():
        if isinstance(appt['appointment_notes'], str):
            for keyword in important_keywords:
                if keyword.lower() in appt['appointment_notes'].lower():
                    alerts.append({
                        'alert_type': 'Important Note Context',
                        'patient_mrn': appt['patient_mrn'],
                        'appointment_date': appt['appointment_date'],
                        'appointment_time': appt['appointment_time'],
                        'appointment_duration': appt['appointment_duration'],
                        'rationale': f'Important keyword "{keyword}" found in notes',
                        'recommended_action': 'Review appointment notes and take appropriate action',
                        'additional_info': appt['appointment_notes']
                    })
    
    return alerts

def check_appointment_durations(df: pd.DataFrame, type_durations: dict) -> list:
    alerts = []
    
    for _, appt in df.iterrows():
        if appt['appointment_type'] in type_durations:
            expected_duration = type_durations[appt['appointment_type']]
            if appt['appointment_duration'] < expected_duration:
                alerts.append({
                    'alert_type': 'Short Appointment Duration',
                    'patient_mrn': appt['patient_mrn'],
                    'appointment_date': appt['appointment_date'],
                    'appointment_time': appt['appointment_time'],
                    'appointment_duration': appt['appointment_duration'],
                    'rationale': f'Appointment duration shorter than expected for {appt["appointment_type"]}',
                    'recommended_action': 'Review and potentially extend appointment duration',
                    'additional_info': f'Expected duration: {expected_duration} minutes'
                })
    
    return alerts

def check_medical_vs_cosmetic(df: pd.DataFrame, cosmetic_keywords: list) -> list:
    alerts = []
    
    for _, appt in df.iterrows():
        if appt['appointment_type'] == 'Medical':
            if isinstance(appt['reason_for_visit'], str):
                for keyword in cosmetic_keywords:
                    if keyword.lower() in appt['reason_for_visit'].lower():
                        alerts.append({
                            'alert_type': 'Potential Cosmetic Appointment',
                            'patient_mrn': appt['patient_mrn'],
                            'appointment_date': appt['appointment_date'],
                            'appointment_time': appt['appointment_time'],
                            'appointment_duration': appt['appointment_duration'],
                            'rationale': f'Medical appointment with cosmetic keyword "{keyword}" in reason for visit',
                            'recommended_action': 'Review and potentially reclassify as cosmetic appointment',
                            'additional_info': appt['reason_for_visit']
                        })
    
    return alerts
