#requires -Version 5.1
param([string]$InstallDir="$HOME\InstagramSocialAgent",[switch]$SkipSetup)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
if(Get-Command py -ErrorAction SilentlyContinue){$p='py';$argsPy=@('-3')}elseif(Get-Command python -ErrorAction SilentlyContinue){$p='python';$argsPy=@()}else{throw 'Install Python 3.10+ first'}
$InstallDir=[IO.Path]::GetFullPath($InstallDir)
$DataDir=Join-Path $InstallDir 'data'
New-Item -ItemType Directory -Force -Path $InstallDir,$DataDir|Out-Null
Copy-Item -LiteralPath (Join-Path $root 'src\social_agent\core.py') -Destination (Join-Path $InstallDir 'social_agent.py') -Force
Copy-Item -LiteralPath (Join-Path $root 'src\social_agent\service.py') -Destination (Join-Path $InstallDir 'social_service.py') -Force
$launcher=Join-Path $InstallDir 'social.cmd'
@"
@echo off
set "SOCIAL_AGENT_HOME=$DataDir"
$p $($argsPy -join ' ') "$InstallDir\social_agent.py" %*
"@|Set-Content -Path $launcher -Encoding ASCII
$serviceLauncher=Join-Path $InstallDir 'service.cmd'
@"
@echo off
set "SOCIAL_AGENT_HOME=$DataDir"
$p $($argsPy -join ' ') "$InstallDir\social_service.py" %*
"@|Set-Content -Path $serviceLauncher -Encoding ASCII
if(-not $SkipSetup){
 $env:SOCIAL_AGENT_HOME=$DataDir
 try {
  & $p @argsPy (Join-Path $InstallDir 'social_agent.py') init
  if($LASTEXITCODE -ne 0){throw 'CLI initialization failed'}
  & $p @argsPy (Join-Path $InstallDir 'social_service.py') setup
  if($LASTEXITCODE -ne 0){throw 'Service initialization failed'}
 } finally {Remove-Item Env:SOCIAL_AGENT_HOME -ErrorAction SilentlyContinue}
}
Write-Host "Installed: $InstallDir" -ForegroundColor Green
Write-Host "Private local data (created for this installation only): $DataDir"
Write-Host "No existing CRM, Maestri workspace, database or credentials were imported."
Write-Host "Use: & '$launcher' draft; & '$serviceLauncher' status"
