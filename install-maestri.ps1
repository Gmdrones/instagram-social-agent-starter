#requires -Version 5.1
param([switch]$OpenOfficialPage)
$ErrorActionPreference = 'Stop'
$official = 'https://www.themaestri.app/pt-br/windows'
Write-Host 'Etapa 1/2 - Maestri oficial'
Write-Host 'Instale o Maestri usando exclusivamente o instalador oficial.'
Write-Host ('Pagina oficial: ' + $official)
if ($OpenOfficialPage) { Start-Process $official }
Write-Host 'Depois execute .\install.ps1 e .\connect-maestri.ps1'
