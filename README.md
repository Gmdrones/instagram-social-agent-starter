# Instagram Social Agent — Community Starter

An open-source, local-first Instagram business workflow starter for **Maestri, Codex, Claude Code and Antigravity**.

**Status: early starter.** Local CRM, niche configuration, editable drafts and a basic Meta API connectivity check are available. **Automatic prospecting, follows, outbound DMs, webhook receiving and automatic Maestri terminal provisioning are NOT implemented.** These features must not be advertised as ready. This is not endorsed by Meta, Instagram or the AI vendors.

## Quick start (Windows)

Requires Python 3.10+ and PowerShell 5.1+.

1. Download this repository as ZIP and extract it.
2. Open PowerShell in the extracted directory.
3. Install Maestri independently using the official site: https://www.themaestri.app/pt-br/windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-maestri.ps1 -OpenOfficialPage
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\connect-maestri.ps1
& "$HOME\InstagramSocialAgent\social.cmd" draft
```

In Maestri, create a Codex, Claude Code or Antigravity terminal, open the installed directory and use the generated `INSTRUCOES-AGENTE.md`. This last step is **manual** in the current release.

## Configure your business and audience

Run `social.cmd init` once. Edit `%USERPROFILE%\.social-agent\config.json` to set your company, niche, website and `message_template`. Available template placeholders: `{company}`, `{niche}`, `{website}`. Example:

```powershell
& "$HOME\InstagramSocialAgent\social.cmd" lead example_business --niche "photography" --source "public website"
& "$HOME\InstagramSocialAgent\social.cmd" list
& "$HOME\InstagramSocialAgent\social.cmd" draft
```

The lead is entered by you and stored locally in SQLite with duplicate prevention. The agent does not search Instagram or message that lead automatically.

## Connect the official Meta API

1. Use an eligible Instagram professional account and create an application at https://developers.facebook.com/.
2. Configure the appropriate Instagram Login/Facebook Login flow, permissions and any required Meta App Review.
3. Follow the official Instagram API setup and webhook documentation.
4. Store the Meta access token **only in your local environment**; never put it in GitHub or in a support message.
5. Set `IG_ACCESS_TOKEN` in the local PowerShell session and run `social.cmd meta-me` to check account connectivity.

**Connectivity is not the same as having messaging/webhook permissions.** A production webhook endpoint, verified inbound event handling, messaging eligibility checks and permission review have not yet been implemented in this starter.

## Limits and compliance

The official API does not offer arbitrary auto-following or unlimited unsolicited cold Direct messaging. Business messaging is subject to user-initiated conversations, approved permissions, applicable messaging windows and platform policies. No tool can promise zero account restrictions. Avoid scraping, unsolicited bulk messaging, evasion, account sharing and anti-abuse bypasses.

## Security

- Credentials and local customer data are not included.
- Local SQLite data is created under `~/.social-agent/`.
- Review PowerShell scripts before running them.
- No administrator privileges, paid services or background services are installed.
- Do not import private files, tokens, real customer lists or sessions from another PC.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Roadmap

Validated Meta webhook receiver, opt-in inbox assistant, safe scheduled reports, configurable audience research through permitted sources, documented Maestri terminal provisioning and a simple setup wizard.

MIT License. Contributions welcome.
