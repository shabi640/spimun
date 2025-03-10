# Chair Login Guide

## Overview

This guide explains how to access the system as a chair delegate. Chair delegates have access to the same chat system as regular delegates but use a special login method to keep their accounts hidden from the regular delegate login process.

## Secret Keys

Chairs log in using special secret keys instead of their actual delegate names. These keys are only known to chairs and administrators:

- **Junior Committee Chair**: `CHAIR_SECRET_KEY_JUNIOR_39129591`
- **Senior Committee Chair**: `CHAIR_SECRET_KEY_SENIOR_73824642`
- **Security Council Chair**: `CHAIR_SECRET_KEY_SC_48375628`

## Login Process

1. Go to the regular login screen
2. Enter your committee's secret key in the "Name" field
3. Select any country (the system will ignore this value)
4. Select any committee (the system will ignore this value)
5. Click "Login"

The system will recognize the secret key in the name field and automatically log you in as the appropriate chair account.

## Security Notes

- Keep your chair secret key confidential
- Do not share these keys with delegates
- Regular delegates cannot find chair accounts through the normal login process
- Chair accounts appear in chats just like regular delegate accounts

## Technical Implementation Details

The chair login system works by:

1. Checking if the provided "name" matches one of the predefined secret keys
2. If it does, looking up the corresponding chair delegate account
3. Logging in with that chair delegate's credentials
4. For regular login attempts, chair accounts are explicitly excluded from search results

## Troubleshooting

If you're having trouble logging in:

1. Verify you're using the correct secret key for your committee
2. Make sure to enter the secret key exactly as shown (with no additional spaces)
3. The entered country and committee don't matter - the system detects chair logins by the secret key alone
4. Contact the system administrator if you continue to have issues

---

**Warning**: Never store these secret keys in client-side code or public repositories. In a production environment, these should be stored securely in environment variables or a secure configuration system.
