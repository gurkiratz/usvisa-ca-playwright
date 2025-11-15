"""
Test script to verify Playwright migration
Run this before fully migrating
"""

from playwright.sync_api import sync_playwright

from settings import *


def test_browser_launch():
    """Test if browser launches correctly"""
    print("Testing browser launch...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://gurkiratz.co")
        print(f"✓ Browser launched successfully")
        print(f"✓ Page title: {page.title()}")
        browser.close()


def test_login_page_load():
    """Test if login page loads"""
    print("\nTesting login page load...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(LOGIN_URL, timeout=30000)

            # Check if email field exists
            email_field = page.locator("#user_email")
            if email_field.is_visible():
                print("✓ Email field found")

            # Check if password field exists
            password_field = page.locator("#user_password")
            if password_field.is_visible():
                print("✓ Password field found")

            print("✓ Login page loaded successfully")
        except Exception as e:
            print(f"✗ Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    print("=== Playwright Migration Test ===\n")
    test_browser_launch()
    test_login_page_load()
    print("\n=== Tests Complete ===")
