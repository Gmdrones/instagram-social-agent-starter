# Instagram Social Agent

Open-source local business assistant for Instagram professional accounts, compatible with **Maestri**, **Codex**, **Claude Code** and **Antigravity**.

## Current implementation

- PowerShell installers for the local assistant; separate official Maestri installer link
- Local SQLite CRM for contacts and lead records (no customer database uploaded to GitHub)
- Customizable business, audience, location and message templates
- Official Meta Instagram API identity connectivity check
- **Webhook server with signed event verification**, duplicate event protection and inbound contact history
- Reply drafting and a review/approval queue
- Official API dispatch of individually approved replies from eligible inbound threads
- Activity reports from stored incoming events and confirmed outgoing API sends
- Unit tests; no compulsory paid services

**Not yet provided:** one-click Maestri terminal provisioning, automated discovery across Instagram profiles, arbitrary follow actions, unsolicited outreach, unattended automatic messaging, production-grade hosted HTTPS webhook deployment, or proof of end-to-end delivery in a live Meta account. Please do not interpret `setup --auto-reply` as enabling automatic sends. The software cannot guarantee no account restrictions.

## Windows installation

Prerequisites: Python 3.10+, PowerShell 5.1+, an Instagram Professional account, and a Meta developer app for messaging features.

1. Install Maestri **separately from its official website** using:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-maestri.ps1 -OpenOfficialPage
```
2. Install the Social Agent:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\connect-maestri.ps1
```
3. Open `%USERPROFILE%\InstagramSocialAgent` in a Codex, Claude Code or Antigravity terminal within Maestri. This part is manual in the current version.
4. Configure your own business:
```powershell
& "$HOME\InstagramSocialAgent\service.cmd" setup --company "Your Business" --niche "your audience" --region "your city" --message "Hello! Thanks for contacting {company}. How can we help?"
& "$HOME\InstagramSocialAgent\service.cmd" status
& "$HOME\InstagramSocialAgent\social.cmd" draft
```
Templates support `{company}`, `{niche}` and `{website}`.

## Meta API connection (required for actual replies)

1. Create your Meta app at https://developers.facebook.com/ and connect an eligible Instagram Professional account.
2. Configure Instagram messaging permissions, app review if applicable, and the subscribed webhook fields as required by the current official documentation.
3. Store `META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_APP_SECRET` and `META_VERIFY_TOKEN` **in your own secure environment**. Never commit them or paste them into issues.
4. Run locally:
```powershell
& "$HOME\InstagramSocialAgent\service.cmd" serve
```
5. Provide a secure public **HTTPS reverse proxy** forwarding `/webhook` to `127.0.0.1:8765`. This repository does not configure a public domain or proxy.
6. Configure Meta webhook verification URL and token in the Meta app, then test with a real incoming message from an eligible conversation.

The webhook validates `X-Hub-Signature-256` using your app secret. Each accepted inbound message is deduplicated, stored in a local CRM and queued as a **draft**.

Review and send an eligible reply:
```powershell
& "$HOME\InstagramSocialAgent\service.cmd" status
& "$HOME\InstagramSocialAgent\service.cmd" approve 1
& "$HOME\InstagramSocialAgent\service.cmd" dispatch 1
& "$HOME\InstagramSocialAgent\service.cmd" report
```
Dispatch only succeeds if Meta accepts the request and returns a message ID. The recipient must meet platform messaging requirements and consent rules. Receiving an event does not by itself guarantee ongoing messaging eligibility.

## Lead workflow

```powershell
& "$HOME\InstagramSocialAgent\social.cmd" lead example_brand --niche "photography" --source "user-provided public website"
& "$HOME\InstagramSocialAgent\social.cmd" list
```

The local CRM can store leads supplied by the operator. **It does not scrape Instagram, automatically follow profiles, or initiate unsolicited DMs.** Planned compliant discovery and qualification should operate on permitted, accessible sources and keep adequate provenance.

## Security and responsible use

- No credentials or personal workspace files included.
- No guaranteed prevention of Instagram restrictions.
- Official supported Meta endpoints only. No scraping, stealth browser outreach or account-limit bypasses.
- Do not expose `/webhook` without signature verification and HTTPS; run locally behind a properly secured public endpoint.
- The server is a reference implementation. For public production hosting, add operational monitoring, token rotation, backups and retry/queue resilience.
- Follow Meta app review, messaging windows, applicable privacy rules and local law.

## Contribute and test

```sh
python -m unittest discover -s tests -v
```

MIT licensed community project. Suggestions and tested contributions are welcome; see `CONTRIBUTING.md` and `SECURITY.md`.
