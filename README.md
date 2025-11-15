# US Visa Appointment Rescheduler (Playwright Version)

Automated tool to monitor and reschedule US visa appointments in Canada.

**Original repository and inspiration:** [kcajc/usvisa-ca](https://github.com/kcajc/usvisa-ca)

## Features

- 🚀 **Playwright-powered**: Fast, reliable browser automation
- 📧 **Email Notifications**: Get notified when appointments are rescheduled
- 🔄 **Auto-retry**: Intelligent retry logic with configurable delays
- 📅 **Date Filtering**: Set acceptable date ranges and exclusions
- 🛡️ **Error Handling**: Robust error handling with screenshots

## Prerequisites

- Python 3.8+
- Playwright (installed via pip)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/gurkiratz/usvisa-ca-playwright
cd usvisa-ca-playwright
```

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

3. Configure your settings in `.env`:

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Configuration

Edit `.env` file with your details:

```env
# Login Credentials
USER_EMAIL=your.email@example.com
USER_PASSWORD=yourpassword
USER_CONSULATE=Toronto

# Date Settings
EARLIEST_ACCEPTABLE_DATE=2025-01-01
LATEST_ACCEPTABLE_DATE=2025-12-31

# Email Settings
GMAIL_EMAIL=sender@gmail.com
GMAIL_APPLICATION_PWD=your_app_password
RECEIVER_EMAIL=receiver@example.com

# Display Settings
SHOW_GUI=False
```

## Usage

```bash
python reschedule_playwright.py
```

## Project Structure

```
usvisa-ca-playwright/
├── reschedule_playwright.py    # Main Playwright script (NEW)
├── playwright_rescheduler.py   # Playwright rescheduling logic (NEW)
├── request_tracker.py          # Request tracking utility
├── settings.py                 # Configuration loader
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
└── legacy/
    └── gmail/                  # Email notification module
```

## Troubleshooting

### Playwright-specific Issues

**Browser not found:**

```bash
playwright install chromium
```

**Screenshots for debugging:**
Error screenshots are automatically saved when rescheduling fails.

**Headless mode issues:**
Set `SHOW_GUI=True` in `.env` to see the browser.

## License

MIT License
