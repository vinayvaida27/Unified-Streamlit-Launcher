param([Parameter(Mandatory=$true)][string]$Path)

$ErrorActionPreference = "Stop"
$Required = @("launcher.exe","config\launcher_config.json","config\platform_manifest.json","apps\apps.json","assets","runtime","docs")
foreach ($item in $Required) {
  $target = Join-Path $Path $item
  if (!(Test-Path $target)) { throw "Release validation failed. Missing $item" }
}
$appCount = (Get-ChildItem (Join-Path $Path "apps") -Directory).Count
if ($appCount -ne 10) { throw "Expected 10 apps, found $appCount" }
Write-Host "Release structure verified."
