from datetime import timedelta

# Time gap threshold
TIME_GAP_THRESHOLD = timedelta(hours=2)

# Standard appointment durations (in minutes)
APPOINTMENT_TYPE_DURATIONS = {
    "New Patient": 30,
    "Follow-up": 15,
    "Cosmetic Consultation": 30,
    "Procedure": 60,
    # Add more appointment types and their standard durations
}

# Keywords to identify cosmetic appointments
COSMETIC_KEYWORDS = [
    "botox", "filler", "laser", "peel", "cosmetic",
    # Add more cosmetic-related keywords
]
