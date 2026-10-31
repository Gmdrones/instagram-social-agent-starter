#requires -Version 5.1
param([string]$InstallDir="$HOME\InstagramSocialAgent")
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$repo='https://github.com/Gmdrones/instagram-social-agent-starter/archive/refs/heads/main.zip'
$tmp=Join-Path $env:TEMP ('social-agent-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $tmp|Out-Null
try {
 $zip=Join-Path $tmp 'source.zip'
 Invoke-WebRequest -Uri $repo -OutFile $zip -UseBasicParsing
 Expand-Archive -LiteralPath $zip -DestinationPath $tmp -Force
 $source=Join-Path $tmp 'instagram-social-agent-starter-main'
 if(-not(Test-Path (Join-Path $source 'install.ps1'))){throw 'Installation files not found'}
 & (Join-Path $source 'install.ps1') -InstallDir $InstallDir
 & (Join-Path $source 'connect-maestri.ps1') -InstallDir $InstallDir
 & (Join-Path $source 'setup-maestri-workspace.ps1') -InstallDir $InstallDir
 Copy-Item -LiteralPath (Join-Path $source 'MAESTRI-PROMPT.md') -Destination (Join-Path $InstallDir 'MAESTRI-PROMPT.md')
 Write-Host 'Install prepared successfully.' -ForegroundColor Green
 Write-Host ('Now open Maestri -> a Maestro terminal and paste the content of '+(Join-Path $InstallDir 'MAESTRI-PROMPT.md'))
 Write-Host 'Maestri must already be installed and you must sign in to your own AI and Instagram accounts.'
}finally {
 Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
