param(
  [switch]$Open
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
  New-Item -ItemType Directory -Force reports\allure-results | Out-Null

  python -m pytest tests\ -v --html=reports\report.html --self-contained-html --alluredir=reports\allure-results

  $allureCmd = Get-Command allure -ErrorAction SilentlyContinue
  if (-not $allureCmd) {
    Write-Host "Allure CLI is not installed (command 'allure' not found)."
    Write-Host "You already have results in: reports\\allure-results"
    Write-Host "Install Allure CLI, then run:"
    Write-Host "  allure generate reports\\allure-results -o reports\\allure-report --clean"
    Write-Host "  allure serve reports\\allure-results"
    exit 0
  }

  allure generate reports\allure-results -o reports\allure-report --clean | Out-Null
  Write-Host "Allure HTML report generated: reports\\allure-report\\index.html"

  if ($Open) {
    allure open reports\allure-report
  }
}
finally {
  Pop-Location
}

