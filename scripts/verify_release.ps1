param([Parameter(Mandatory=$true)][string]$Path)

$ErrorActionPreference = "Stop"
$Required = @("launcher.exe","launcher_config.json","platform_manifest.json","apps","assets","runtime","documentation")
foreach ($item in $Required) {
  $target = Join-Path $Path $item
  if (!(Test-Path $target)) { throw "Release validation failed. Missing $item" }
}
$appCount = (Get-ChildItem (Join-Path $Path "apps") -Directory).Count
if ($appCount -ne 10) { throw "Expected 10 apps, found $appCount" }
Write-Host "Release structure verified."
