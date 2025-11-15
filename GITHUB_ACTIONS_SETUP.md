# GitHub Actions Setup Guide

This guide walks you through setting up automated US visa appointment monitoring using GitHub Actions.

## Overview

The GitHub Actions workflow automatically:

- Runs daily at 7 PM EST (12 AM UTC)
- Checks for available visa appointment dates
- Reschedules to earlier dates when found
- Sends email notifications on success
- Captures screenshots on errors for debugging

## Prerequisites

- GitHub repository with this code
- Gmail account for notifications
- US visa appointment account

## Setup Steps

### 1. Enable GitHub Actions

The workflow file is already included at `.github/workflows/playwright.yml`. It will automatically activate when you push to the `main` branch.

### 2. Configure Repository Secrets

Repository secrets keep your credentials secure. Never commit actual passwords to your code.

**To add secrets:**

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret from the table below

### 3. Required Secrets

| Secret Name                | Description                     | Example Value               |
| -------------------------- | ------------------------------- | --------------------------- |
| `USER_EMAIL`               | Your visa account email         | `your.email@example.com`    |
| `USER_PASSWORD`            | Your visa account password      | `yourpassword`              |
| `USER_CONSULATE`           | Consulate city                  | `Toronto`                   |
| `NUM_PARTICIPANTS`         | Number of participants          | `1`                         |
| `EARLIEST_ACCEPTABLE_DATE` | Earliest date you'll accept     | `2025-08-10`                |
| `LATEST_ACCEPTABLE_DATE`   | Latest date you'll accept       | `2026-05-10`                |
| `GMAIL_SENDER_NAME`        | Email sender name               | `Visa Appointment Reminder` |
| `GMAIL_EMAIL`              | Gmail account for notifications | `your.gmail@gmail.com`      |
| `GMAIL_APPLICATION_PWD`    | Gmail app password (16 chars)   | `abcd efgh ijkl mnop`       |
| `RECEIVER_NAME`            | Notification recipient name     | `Your Name`                 |
| `RECEIVER_EMAIL`           | Email to receive notifications  | `notifications@example.com` |

### 4. Gmail App Password Setup

Gmail requires an application-specific password for automated access:

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google App Passwords](https://security.google.com/settings/security/apppasswords)
3. Select **Mail** as the app
4. Generate a new app password
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)
6. Use this password as the `GMAIL_APPLICATION_PWD` secret

> **Note:** Never use your regular Gmail password for this.

## Workflow Triggers

The automation runs in these scenarios:

### Automatic Triggers

- **Daily Schedule**: Every day at 7 PM EST (12 AM UTC)
- **Code Push**: When you push to the `main` branch
- **Pull Request**: When someone creates a PR (for testing)

### Manual Trigger

1. Go to the **Actions** tab in your repository
2. Select "US Visa Rescheduler" workflow
3. Click **Run workflow**
4. Click **Run workflow** button

## Monitoring & Debugging

### View Workflow Runs

1. Go to **Actions** tab in your repository
2. Click on any workflow run to see details
3. Expand steps to view detailed logs

### Email Notifications

You'll receive emails when:

- ✅ Appointment successfully rescheduled
- ❌ Workflow encounters errors
- 📧 Program exits (with reason)

### Error Screenshots

If the workflow fails:

1. Click on the failed workflow run
2. Scroll to **Artifacts** section
3. Download `rescheduler-screenshots-{run-number}.zip`
4. Screenshots help debug what went wrong

### Common Issues

**Workflow not running:**

- Check if repository secrets are set correctly
- Verify workflow file exists in `.github/workflows/`
- Ensure you have Actions enabled in repository settings

**Login failures:**

- Double-check `USER_EMAIL` and `USER_PASSWORD`
- Ensure account isn't locked due to multiple login attempts

**Email not sending:**

- Verify Gmail app password is correct (16 characters)
- Check `GMAIL_EMAIL` and `RECEIVER_EMAIL` are valid
- Ensure 2FA is enabled on Gmail account

**No available dates:**

- Check your date range (`EARLIEST_ACCEPTABLE_DATE` to `LATEST_ACCEPTABLE_DATE`)
- Monitor workflow logs to see what dates are available
- Consider expanding your acceptable date range

## Workflow Features

### Security

- ✅ All credentials stored as encrypted repository secrets
- ✅ Runs in isolated GitHub-hosted environment
- ✅ No sensitive data in logs or code

### Performance

- ✅ Dependency caching for faster runs
- ✅ 30-minute timeout prevents infinite runs
- ✅ Optimized for headless browser operation

### Monitoring

- ✅ Detailed logging of all steps
- ✅ Screenshot capture on failures
- ✅ Email notifications for important events
- ✅ Artifact cleanup after 7 days

## Advanced Configuration

### Customizing Schedule

To change when the workflow runs, edit the cron expression in `.github/workflows/playwright.yml`:

```yaml
schedule:
  - cron: '0 0 * * *' # 7 PM EST daily
```

[Use crontab.guru](https://crontab.guru/) to generate different schedules.

### Adding Date Exclusions

Add exclusion date ranges in your repository secrets:

- `EXCLUSION_START_DATE_1` and `EXCLUSION_END_DATE_1`
- `EXCLUSION_START_DATE_2` and `EXCLUSION_END_DATE_2`
- Up to 9 exclusion ranges supported

### Testing Changes

1. Make changes to your code
2. Push to `main` branch
3. Workflow runs automatically for testing
4. Check Actions tab for results

## Security Best Practices

- ✅ Never commit passwords or credentials to code
- ✅ Use repository secrets for all sensitive data
- ✅ Regularly rotate your Gmail app password
- ✅ Monitor workflow runs for unusual activity
- ✅ Keep your visa account secure with strong password

## Support

If you encounter issues:

1. Check workflow logs in Actions tab
2. Review this setup guide
3. Verify all secrets are configured correctly
4. Test with manual workflow trigger first
5. Check email spam folder for notifications

## Troubleshooting Checklist

- [ ] All 11 repository secrets are set
- [ ] Gmail app password is 16 characters (no spaces in secret)
- [ ] 2FA enabled on Gmail account
- [ ] Date range is reasonable (not too restrictive)
- [ ] Workflow file exists in `.github/workflows/playwright.yml`
- [ ] Actions are enabled in repository settings
- [ ] No syntax errors in workflow file

---

**Happy automated appointment hunting! 🎯**
