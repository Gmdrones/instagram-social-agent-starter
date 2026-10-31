#requires -Version 5.1
param([string]$InstallDir="$HOME\InstagramSocialAgent")
$ErrorActionPreference='Stop'
if(-not(Test-Path(Join-Path $InstallDir 'social.cmd'))){throw 'Run install.ps1 first'}
$guide=Join-Path $InstallDir 'INSTRUCOES-AGENTE.md'
@'
# Instagram Social Agent - Independent Maestri workspace
This is a new independent install. Do not connect to the publisher's projects, data, tokens, machines, CRM, or Maestri workspace.
Open THIS installed directory in your own new Maestri terminal (Codex, Claude Code, or Antigravity).
The agent's local data resides in the data subfolder, created on this computer.
Run social.cmd draft, social.cmd list, service.cmd status, service.cmd setup --company "My Company" --niche "my niche".
Configure YOUR OWN Meta developer app, Instagram professional account, token, app secret and webhook.
Never print secret environment variables or claim messaging was sent without Meta API confirmation.
Automatic terminal provisioning and unrestricted outbound Directs are not included.
'@|Set-Content -LiteralPath $guide -Encoding UTF8
Write-Host "Local setup guide: $guide"
Write-Host 'Create a new Maestri terminal and open this installed folder.'
