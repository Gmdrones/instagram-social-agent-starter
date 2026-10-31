#requires -Version 5.1
param([string]$InstallDir="$HOME\InstagramSocialAgent")
$ErrorActionPreference='Stop'
if(-not(Test-Path(Join-Path $InstallDir 'social.cmd'))){throw 'Run install.ps1 first'}
$guide=Join-Path $InstallDir 'INSTRUCOES-AGENTE.md'
@'
# Instagram Social Agent — Maestri
Open this directory in a Codex, Claude Code, or Antigravity terminal inside Maestri.
Run social.cmd init, social.cmd list, social.cmd draft, and social.cmd meta-me.
Customize local config.json for company, audience, and message template.
Never print secrets or claim an action was sent without Meta API confirmation.
The starter does not automatically provision Maestri terminals, send DMs, follow profiles or install a webhook receiver.
'@|Set-Content -LiteralPath $guide -Encoding UTF8
Write-Host "Guide created: $guide"
Write-Host 'Open the installed folder in a Maestri AI terminal.'
