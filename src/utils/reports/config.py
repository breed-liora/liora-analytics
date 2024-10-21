# Login credentials
USERNAME = "breed.admin"
PASSWORD = "Barricreed88v2"

# Base URLs
EMA_LOGIN_URL = "https://sso.ema.md/auth/realms/Modmed/protocol/openid-connect/auth?response_type=code&client_id=ema&redirect_uri=https%3A%2F%2Flioraderm.ema.md%2Fema%2Fsso%2Flogin&state=63bdedb4-a7be-4a7c-81a9-b70e64a45e21&login=true&login_hint=UkVWSVNJT049ZDQwYjYxOWNkOTtET01BSU49bGlvcmFkZXJtLmVtYS5tZDtGSVJNX0xPR089bnVsbDtGSVJNX05BTUU9TGlvcmEgRGVybWF0b2xvZ3kgJiBBZXN0aGV0aWNzO09GRkxJTkVfQUNDRVNTPUZBTFNFO01FRElDQUxfRE9NQUlOPWRlcm1hdG9sb2d5O0dEUFJfQ09PS0lFPXByb3ZpZGVyO09SSUdJTj0vZW1hL1Byb3ZpZGVyTG9naW4uYWN0aW9uO01BUktFVElOR19CQU5ORVI9VFJVRTtWRVJTSU9OPTcuNi42O0ZJUk1fR0xPQkFMX0lEPTExMzk4MztHRFBSPVRSVUU7TU9CSUxFPUZBTFNF&scope=openid"
EMA_FINANCIALS_URL = "https://lioraderm.ema.md/ema/practice/reports/Reports.action#/reports/financials"

class EMA_ANALYTICS_URLS:
    # Financial reports
    FINANCIALS_PAYMENTS_POSTED="https://qlikembedding.ema.md/ema/sense/app/574e61d2-da59-4c43-94a9-0cc8bf1ae813/sheet/JsLSVX/state/analysis"
    FINANCIALS_APPOINTMENTS_CUSTOM="https://qlikembedding.ema.md/ema/sense/app/574e61d2-da59-4c43-94a9-0cc8bf1ae813/sheet/EZcvm/state/analysis"

    # Clinical / Operational reports
    ## Potentially use this to get a list of all patients, treatments, and service dates
    CLINICAL_PRACTICE_CENSUS_CUSTOM="https://qlikembedding.ema.md/ema/sense/app/12abf690-b971-42f4-b2f0-7c29f113883e/sheet/JmAHqa/state/analysis"

    # Inventory reports
    INVENTORY_PRODUCTS_SOLD="https://qlikembedding.ema.md/ema/sense/app/0bff8a88-7f93-4ab2-a170-fc16276a8ca6/sheet/5c56ec24-e87c-471c-bed7-0fe69a3567f9/state/analysis"
    INVENTORY_STOCK_SUMMARY="https://qlikembedding.ema.md/ema/sense/app/0bff8a88-7f93-4ab2-a170-fc16276a8ca6/sheet/5413bed8-c308-4f0c-bfd2-3bfff44d1686/state/analysis"    

    # Data Explorer


# Report configurations
# "qlik_name" is the name of the report as it appears in Qlik and is used to verify the report is loaded
REPORTS = {
    "payments_posted_by_date": {
        "name": "payments_posted_by_date",
        "qlik_name": "Payments Posted",
        "url": EMA_ANALYTICS_URLS.FINANCIALS_PAYMENTS_POSTED,
        "dimensions": [
            "Posted Date",
            "Posted Date Month/Year",
            "Posted Date Quarter/Year",
        ],
        "measures": [
            "Charges",
            "Payment Amount"
        ]
    },
    "appointments_by_date": {
        "name": "appointments_by_date",
        "qlik_name": "Appointments Custom",
        "url": EMA_ANALYTICS_URLS.FINANCIALS_APPOINTMENTS_CUSTOM,
        "dimensions": [
            "Patient MRN",
            "New Patient Indicator",
            "Appointment Date",
            "Appointment Time",
            "Appointment Duration",
            "Appointment Type",
            "Appointment Status",
            "Reason for Visit",
            "Patient Has Future Appointment?",
            "Appointment Notes",
            "Primary Provider",
            "Appointment Created By",
            "Policy Type",
            "Insurance Eligibility Status",
        ],
        "measures": [
            "Patient Count (Unique)"
        ]
    }
}