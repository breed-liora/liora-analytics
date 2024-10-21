import unittest
from datetime import datetime, timedelta
import pandas as pd
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

class TestAppointmentUtils(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.sample_df = pd.DataFrame({
            'appointment_date': [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)],
            'appointment_time': [datetime(2024, 1, 1, 9, 0), datetime(2024, 1, 2, 10, 0), datetime(2024, 1, 3, 14, 0)],
            'appointment_duration': [30, 15, 60],
            'appointment_type': ['New Patient', 'Follow-up', 'Procedure'],
            'appointment_notes': ['First visit', 'Regular checkup', 'Botox treatment'],
            'patient_mrn': [1, 2, 3],
            'reason_for_visit': ['New patient consultation', 'Follow-up visit', 'Cosmetic procedure']
        })

    def test_filter_appointments(self):
        filtered_df = filter_appointments(self.sample_df)
        self.assertGreater(len(filtered_df), 0)
        self.assertTrue(all(filtered_df['appointment_date'] > datetime.now().date()))
        self.assertTrue(all(filtered_df['appointment_date'] <= datetime.now().date() + timedelta(days=30)))

    def test_check_time_gaps(self):
        alerts = check_time_gaps(self.sample_df, TIME_GAP_THRESHOLD)
        self.assertIsInstance(alerts, list)
        # Add more specific assertions based on your expected behavior

    def test_check_appointment_types(self):
        alerts = check_appointment_types(self.sample_df, APPOINTMENT_TYPE_DURATIONS)
        self.assertIsInstance(alerts, list)
        # Add more specific assertions based on your expected behavior

    def test_check_appointment_notes(self):
        alerts = check_appointment_notes(self.sample_df)
        self.assertIsInstance(alerts, list)
        # Add more specific assertions based on your expected behavior

    def test_check_appointment_durations(self):
        alerts = check_appointment_durations(self.sample_df, APPOINTMENT_TYPE_DURATIONS)
        self.assertIsInstance(alerts, list)
        # Add more specific assertions based on your expected behavior

    def test_check_medical_vs_cosmetic(self):
        alerts = check_medical_vs_cosmetic(self.sample_df, COSMETIC_KEYWORDS)
        self.assertIsInstance(alerts, list)
        # Add more specific assertions based on your expected behavior

if __name__ == '__main__':
    unittest.main()
