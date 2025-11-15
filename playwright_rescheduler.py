from datetime import date, datetime
from time import sleep

from playwright.sync_api import Page

from settings import *


def log_message(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def playwright_reschedule(page: Page, new_date: date) -> bool:
    """
    Reschedule appointment to the new date using Playwright

    Args:
        page: Playwright page object
        new_date: The date to reschedule to

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        log_message(f"Starting rescheduling process for {new_date}")

        # Click reschedule appointment button
        page.click('a:has-text("Reschedule Appointment")')
        page.wait_for_load_state("networkidle")
        sleep(1)

        # Select the date input field
        date_input = page.locator("#appointments_consulate_appointment_date")
        date_input.click()

        # Format date for input (YYYY-MM-DD)
        date_str = new_date.strftime("%Y-%m-%d")

        # Clear and fill the date
        date_input.fill(date_str)
        sleep(1)

        # Wait for available times to load
        page.wait_for_selector(
            '#appointments_consulate_appointment_time option:not([value=""])',
            timeout=10000,
        )

        # Get available time slots
        time_options = page.locator(
            '#appointments_consulate_appointment_time option:not([value=""])'
        ).all()

        if not time_options:
            log_message("No time slots available for selected date")
            return False

        # Select first available time
        first_time = time_options[0].get_attribute("value")
        page.select_option("#appointments_consulate_appointment_time", first_time)
        log_message(f"Selected time: {first_time}")
        sleep(1)

        # Click submit/continue button
        page.click('input[name="commit"]')
        page.wait_for_load_state("networkidle")
        sleep(2)

        # Confirm the appointment
        confirm_button = page.locator('a.button.alert:has-text("Confirm")')
        if confirm_button.is_visible():
            confirm_button.click()
            page.wait_for_load_state("networkidle")
            sleep(2)
            log_message("Appointment confirmed")

        # Verify success
        success_message = page.locator(".alert-box.success, .alert.alert-success")
        if success_message.is_visible():
            log_message("Rescheduling successful!")
            return True

        log_message("Could not verify successful rescheduling")
        return False

    except Exception as e:
        log_message(f"Error during rescheduling: {e}")
        # Take screenshot for debugging
        try:
            screenshot_path = (
                f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            page.screenshot(path=screenshot_path)
            log_message(f"Screenshot saved to {screenshot_path}")
        except:
            pass
        return False
