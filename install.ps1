#requires -Version 5.1
param([string]$InstallDir = "$HOME\InstagramSocialAgent",[switch]$SkipSetup)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
$py=Get-Command py -ErrorAction SilentlyContinue
if($py){$p='py';$argsPy=@('-3')}else{$p='python';$argsPy=@();if(-not(Get-Command python -ErrorAction SilentlyContinue)){throw 'Install Python 3.10+ first'}}
New-Item -ItemType Directory -Force -Path $InstallDir|Out-Null
$dest=Join-Path $InstallDir 'social_agent.py'
Copy-Item -LiteralPath (Join-Path $root 'src\social_agent\core.py') -Destination $dest -Force
$launcher=Join-Path $InstallDir 'social.cmd'
@"
@echo off
$p $($argsPy -join ' ') "$dest" %*
"@|Set-Content -Path $launcher -Encoding ASCII
if(-not $SkipSetup){& $p @argsPy $dest init}
Write-Host "Installed: $InstallDir" -ForegroundColor Green
Write-Host "Try: & '$launcher' draft"
