#requires -Version 5.1
param([string]$InstallDir="$HOME\InstagramSocialAgent",[switch]$SkipSetup)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
if(Get-Command py -ErrorAction SilentlyContinue){$p='py';$argsPy=@('-3')}elseif(Get-Command python -ErrorAction SilentlyContinue){$p='python';$argsPy=@()}else{throw 'Install Python 3.10+ first'}
New-Item -ItemType Directory -Force -Path $InstallDir|Out-Null
Copy-Item -LiteralPath (Join-Path $root 'src\social_agent\core.py') -Destination (Join-Path $InstallDir 'social_agent.py') -Force
Copy-Item -LiteralPath (Join-Path $root 'src\social_agent\service.py') -Destination (Join-Path $InstallDir 'social_service.py') -Force
$launcher=Join-Path $InstallDir 'social.cmd'
@"
@echo off
$p $($argsPy -join ' ') "$InstallDir\social_agent.py" %*
"@|Set-Content -Path $launcher -Encoding ASCII
$serviceLauncher=Join-Path $InstallDir 'service.cmd'
@"
@echo off
$p $($argsPy -join ' ') "$InstallDir\social_service.py" %*
"@|Set-Content -Path $serviceLauncher -Encoding ASCII
if(-not $SkipSetup){
 & $p @argsPy (Join-Path $InstallDir 'social_agent.py') init
 & $p @argsPy (Join-Path $InstallDir 'social_service.py') setup
}
Write-Host "Installed: $InstallDir" -ForegroundColor Green
Write-Host "Draft: & '$launcher' draft"
Write-Host "Service: & '$serviceLauncher' status"
Write-Host "Configure Meta tokens securely using local process environment variables."
