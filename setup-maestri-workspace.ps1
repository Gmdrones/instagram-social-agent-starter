#requires -Version 5.1
param([string]$InstallDir="$HOME\InstagramSocialAgent",[switch]$OpenInstagram)
$ErrorActionPreference='Stop'
if(-not(Test-Path (Join-Path $InstallDir 'service.cmd'))){throw 'Run install.ps1 first'}
$guide=Join-Path $InstallDir 'MAESTRI-BOOTSTRAP.md'
@'
# One-time Maestri setup (user-owned workspace only)

Prerequisites: install and open Maestri, connect your own Codex/Claude Code/Antigravity account, start a new Maestro session. Never use a publisher's account or browser profile.

Paste the following into YOUR OWN Maestro terminal (not a shell) to create a team using the native recruit command. Preset names and availability depend on the installed Maestri version.

1. Check 'maestri recruit --help' and 'maestri list'.
2. Create an assistant named "Social Research" using your chosen AI preset, with --dir pointing at the folder containing social.cmd.
3. Create an assistant named "Social CRM" to manage local SQLite records and candidate reviews.
4. Create an assistant named "Social Browser" for the Instagram portal, using 'maestri portal create https://www.instagram.com/ "My Instagram"'.
5. Ask the user to sign in manually in the new portal; never request credentials or 2FA codes in chat.
6. Connect the teammates, and ask the agents to read INSTRUCOES-AGENTE.md.
7. Do not use any of the publisher's workspaces, databases, cloud accounts, tokens, terminal IDs or browser sessions.
8. Enable scheduled research from an agent only after the user selects a niche, location and search API credentials.
9. Keep follow actions and unsolicited outbound Directs manual. Only official Meta-approved messaging may be dispatched, within eligibility checks.

If the recruit or portal command is not available to this Maestri version, stop with a clear message rather than modifying internal workspace JSON or existing sessions.
'@|Set-Content -LiteralPath $guide -Encoding UTF8
Write-Host "Prepared independent Maestri setup guide: $guide"
if($OpenInstagram){Start-Process 'https://www.instagram.com/'}
Write-Host 'Open your own Maestro terminal and paste the instructions from this file.'
