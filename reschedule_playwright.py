import re
import traceback
from datetime import datetime
from time import sleep
from typing import Union, List

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from legacy.gmail import GMail, Message
from playwright_rescheduler import playwright_reschedule
from request_tracker import RequestTracker
from settings import *


def log_message(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def get_browser_context(playwright):
    """Initialize Playwright browser with context"""
    browser = playwright.chromium.launch(
        headless=PLAYWRIGHT_HEADLESS,
        slow_mo=PLAYWRIGHT_SLOW_MO if not PLAYWRIGHT_HEADLESS else 0,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="America/Toronto",
    )

    return browser, context


def login(page: Page) -> None:
    """Login to the visa appointment system"""
    page.goto(LOGIN_URL)

    # Fill email
    page.fill("#user_email", USER_EMAIL)

    # Fill password
    page.fill("#user_password", USER_PASSWORD)

    # Click policy checkbox
    page.click(".icheckbox")

    # Click login button
    page.click('input[name="commit"]')

    # Wait for navigation
    page.wait_for_load_state("networkidle")


def get_appointment_page(page: Page) -> None:
    """Navigate to appointment page"""
    # Click continue button
    page.click('a:has-text("Continue")')

    # Wait for navigation
    page.wait_for_load_state("networkidle")
    sleep(2)

    # Extract ID from URL and navigate to appointment page
    current_url = page.url
    url_id = re.search(r"/(\d+)", current_url).group(1)
    appointment_url = APPOINTMENT_PAGE_URL.format(id=url_id)
    page.goto(appointment_url)
    page.wait_for_load_state("networkidle")


def get_available_dates(
    page: Page, request_tracker: RequestTracker
) -> Union[List[datetime.date], None]:
    """Fetch available dates using Playwright's API request context"""
    request_tracker.log_retry()
    request_tracker.retry()

    current_url = page.url
    request_url = current_url + AVAILABLE_DATE_REQUEST_SUFFIX

    try:
        # Use Playwright's request context for API calls
        response = page.context.request.get(
            request_url,
            headers={
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": current_url,
            },
        )

        if response.status != 200:
            log_message(f"Failed with status code {response.status}")
            log_message(f"Response Text: {response.text()}")
            return None

        dates_json = response.json()
        dates = [
            datetime.strptime(item["date"], "%Y-%m-%d").date() for item in dates_json
        ]
        return dates

    except Exception as e:
        log_message(f"Get available dates request failed: {e}")
        return None


def is_date_excluded(date: datetime.date) -> bool:
    """Check if date falls in any excluded range"""
    for start, end in EXCLUSION_DATE_RANGES:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if start_date <= date <= end_date:
            log_message(f"Date falls in excluded range: {start} to {end}")
            return True
    return False


def send_email_notification(subject: str, body: str) -> None:
    """Send email notification"""
    try:
        gmail = GMail(f"{GMAIL_SENDER_NAME} <{GMAIL_EMAIL}>", GMAIL_APPLICATION_PWD)
        msg = Message(subject, to=f"{RECEIVER_NAME} <{RECEIVER_EMAIL}>", text=body)
        gmail.send(msg)
        gmail.close()
    except Exception as e:
        log_message(f"Failed to send email: {e}")


def reschedule(page: Page, retry_count: int = 0) -> bool:
    """Main rescheduling logic"""
    date_request_tracker = RequestTracker(
        retry_count if retry_count > 0 else DATE_REQUEST_MAX_RETRY,
        DATE_REQUEST_DELAY * retry_count if retry_count > 0 else DATE_REQUEST_MAX_TIME,
    )

    while date_request_tracker.should_retry():
        dates = get_available_dates(page, date_request_tracker)

        if not dates:
            log_message("Error occurred when requesting available dates")
            sleep(DATE_REQUEST_DELAY)
            continue

        earliest_available_date = dates[0]
        earliest_acceptable_date = datetime.strptime(
            EARLIEST_ACCEPTABLE_DATE, "%Y-%m-%d"
        ).date()
        latest_acceptable_date = datetime.strptime(
            LATEST_ACCEPTABLE_DATE, "%Y-%m-%d"
        ).date()

        if (
            earliest_acceptable_date
            <= earliest_available_date
            <= latest_acceptable_date
        ):
            # Check exclusion ranges
            if is_date_excluded(earliest_available_date):
                sleep(DATE_REQUEST_DELAY)
                continue

            log_message(f"FOUND SLOT ON {earliest_available_date}!!!")

            try:
                if playwright_reschedule(page, earliest_available_date):
                    send_email_notification(
                        f"Visa Appointment Rescheduled for {earliest_available_date}",
                        f"Your visa appointment has been successfully rescheduled to {earliest_available_date} at {USER_CONSULATE} consulate.",
                    )
                    log_message("SUCCESSFULLY RESCHEDULED!!!")
                    return True
                return False
            except Exception as e:
                log_message(f"Rescheduling failed: {e}")
                traceback.print_exc()
                continue
        else:
            log_message(f"Earliest available date is {earliest_available_date}")

        sleep(DATE_REQUEST_DELAY)

    return False


def reschedule_with_new_session(
    playwright, retry_count: int = DATE_REQUEST_MAX_RETRY
) -> bool:
    """Create new browser session and attempt rescheduling"""
    browser, context = get_browser_context(playwright)
    page = context.new_page()

    session_failures = 0
    while session_failures < NEW_SESSION_AFTER_FAILURES:
        try:
            login(page)
            get_appointment_page(page)
            break
        except Exception as e:
            log_message(f"Unable to get appointment page: {e}")
            session_failures += 1
            sleep(FAIL_RETRY_DELAY)
            if session_failures >= NEW_SESSION_AFTER_FAILURES:
                context.close()
                browser.close()
                return False
            continue

    rescheduled = reschedule(page, retry_count)

    # Cleanup
    context.close()
    browser.close()

    return rescheduled


def main():
    """Main execution function"""
    session_count = 0
    log_message(f"Attempting to reschedule for email: {USER_EMAIL}")
    log_message(f"User Consulate: {USER_CONSULATE}")
    log_message(f"Earliest Acceptable Date: {EARLIEST_ACCEPTABLE_DATE}")
    log_message(f"Latest Acceptable Date: {LATEST_ACCEPTABLE_DATE}")

    if EXCLUSION_DATE_RANGES:
        log_message("Excluded Date Ranges:")
        for i, (start, end) in enumerate(EXCLUSION_DATE_RANGES, 1):
            log_message(f"  Range {i}: {start} to {end}")
    else:
        log_message("No date ranges excluded")

    with sync_playwright() as playwright:
        while True:
            session_count += 1
            log_message(f"Attempting with new session #{session_count}")
            rescheduled = reschedule_with_new_session(
                playwright, DATE_REQUEST_MAX_RETRY
            )
            sleep(NEW_SESSION_DELAY)
            if rescheduled:
                break

    send_email_notification(
        "Rescheduler Program Exited",
        f"The rescheduler program has exited on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
    )


if __name__ == "__main__":
    main()
