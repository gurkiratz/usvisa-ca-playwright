import os
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Account Info
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")
NUM_PARTICIPANTS = 1

# Say you want an appointment no later than Mar 14, 2024
# Please strictly follow the YYYY-MM-DD format for all dates

EARLIEST_ACCEPTABLE_DATE = os.getenv("EARLIEST_ACCEPTABLE_DATE")
LATEST_ACCEPTABLE_DATE = os.getenv("LATEST_ACCEPTABLE_DATE")

# Date exclusion ranges
EXCLUSION_DATE_RANGES = []
if EARLIEST_ACCEPTABLE_DATE and LATEST_ACCEPTABLE_DATE:
    try:
        earliest_acceptable_date = datetime.strptime(
            EARLIEST_ACCEPTABLE_DATE, "%Y-%m-%d"
        ).date()
        latest_acceptable_date = datetime.strptime(
            LATEST_ACCEPTABLE_DATE, "%Y-%m-%d"
        ).date()

        for i in range(1, 10):  # Support up to 9 exclusion ranges
            start = os.getenv(f"EXCLUSION_START_DATE_{i}")
            end = os.getenv(f"EXCLUSION_END_DATE_{i}")
            if start and end:
                try:
                    exclusion_start_date = datetime.strptime(start, "%Y-%m-%d").date()
                    exclusion_end_date = datetime.strptime(end, "%Y-%m-%d").date()
                    if (
                        exclusion_start_date < exclusion_end_date
                        and exclusion_start_date > earliest_acceptable_date
                        and exclusion_end_date < latest_acceptable_date
                    ):
                        EXCLUSION_DATE_RANGES.append((start, end))
                except ValueError:
                    print(f"Invalid date format in exclusion range {start} to {end}")
    except ValueError:
        print(
            "Invalid date format in EARLIEST_ACCEPTABLE_DATE or LATEST_ACCEPTABLE_DATE"
        )

# Your consulate's city
CONSULATES = {
    "Calgary": 89,
    "Halifax": 90,
    "Montreal": 91,
    "Ottawa": 92,
    "Quebec": 93,
    "Toronto": 94,
    "Vancouver": 95,
}  # Only Toronto and Vancouver consulates are verified
# Choose a city from the list above
USER_CONSULATE = os.getenv("USER_CONSULATE", "Toronto")

# The following is only required for the Gmail notification feature
# Gmail login info
GMAIL_SENDER_NAME = os.getenv("GMAIL_SENDER_NAME")
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APPLICATION_PWD = os.getenv("GMAIL_APPLICATION_PWD")

# Email notification receiver info
RECEIVER_NAME = os.getenv("RECEIVER_NAME")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Override with local, for developers
# from local import *

# See the automation in action
SHOW_GUI = True  # toggle to false if you don't want to see the browser

# If you just want to see the program run WITHOUT clicking the confirm reschedule button
# For testing, also set a date really far away so the app actually tries to reschedule
TEST_MODE = True

# Don't change the following unless you know what you are doing
DETACH = True
NEW_SESSION_AFTER_FAILURES = 5  # Creates a fresh browser session after 5 consecutive failures. This helps reset cookies, browser state, and potential blocking.
NEW_SESSION_DELAY = 300  # Wait 5 minutes (300 seconds) before starting a new session. Prevents aggressive retries that might trigger rate limiting.
TIMEOUT = 10  # General timeout for operations (10 seconds). Used for page loads, element waits, etc.
FAIL_RETRY_DELAY = (
    180  # Wait 3 minutes (180 seconds) after a generalfailure before retrying.
)
DATE_REQUEST_DELAY = 180  # Wait 3 minutes between each request for available dates.
DATE_REQUEST_MAX_RETRY = 5
DATE_REQUEST_MAX_TIME = 15 * 60
LOGIN_URL = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
AVAILABLE_DATE_REQUEST_SUFFIX = (
    f"/days/{CONSULATES[USER_CONSULATE]}.json?appointments[expedite]=false"
)
APPOINTMENT_PAGE_URL = "https://ais.usvisa-info.com/en-ca/niv/schedule/{id}/appointment"
PAYMENT_PAGE_URL = "https://ais.usvisa-info.com/en-ca/niv/schedule/{id}/payment"
REQUEST_HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
}

# Typical flow:
# 1. Check for dates every 3 minutes (DATE_REQUEST_DELAY)
# 2. If 5 failures occur (DATE_REQUEST_MAX_RETRY), wait 5 minutes (NEW_SESSION_DELAY)
# 3. Start fresh browser session after 5 session failures (NEW_SESSION_AFTER_FAILURES)
# 4. Each session runs max 15 minutes (DATE_REQUEST_MAX_TIME)

# Playwright Settings
PLAYWRIGHT_SLOW_MO = 50  # Slow down by 100ms per action for visibility
PLAYWRIGHT_TIMEOUT = TIMEOUT * 1000  # Convert to milliseconds
# Read PLAYWRIGHT_HEADLESS from environment, with fallback to SHOW_GUI
# In CI/GitHub Actions, PLAYWRIGHT_HEADLESS should be explicitly set to 'true'
PLAYWRIGHT_HEADLESS_ENV = os.getenv("PLAYWRIGHT_HEADLESS", "").lower()
if PLAYWRIGHT_HEADLESS_ENV in ("true", "1", "yes"):
    PLAYWRIGHT_HEADLESS = True
elif PLAYWRIGHT_HEADLESS_ENV in ("false", "0", "no"):
    PLAYWRIGHT_HEADLESS = False
else:
    # Fallback: use inverse of SHOW_GUI
    PLAYWRIGHT_HEADLESS = not SHOW_GUI
