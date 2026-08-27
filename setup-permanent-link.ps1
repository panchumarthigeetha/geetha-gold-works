$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$ngrok = Join-Path $Root "ngrok.exe"
$domainFile = Join-Path $Root "data\permanent-domain.txt"

Write-Host ""
Write-Host "Geetha Gold Works - Permanent public link" -ForegroundColor Cyan
Write-Host "This creates one website address that stays the same." -ForegroundColor Gray
Write-Host ""

Write-Host "Step 1: Create a FREE ngrok account (one time)."
Write-Host "A browser page will open. Sign up, then come back here."
Start-Process "https://dashboard.ngrok.com/signup"
Read-Host "Press Enter after you have signed in"

Write-Host ""
Write-Host "Step 2: Copy your authtoken."
Start-Process "https://dashboard.ngrok.com/get-started/your-authtoken"
$token = Read-Host "Paste your authtoken here"
if (-not $token) {
    Write-Host "No authtoken entered." -ForegroundColor Red
    exit 1
}

& $ngrok config add-authtoken $token | Out-Host

Write-Host ""
Write-Host "Step 3: Claim your FREE static domain (this is the permanent website address)."
Start-Process "https://dashboard.ngrok.com/domains"
Write-Host "Click 'New Domain', then copy it. It looks like: something.ngrok-free.app"
$domain = (Read-Host "Paste your domain here").Trim()
$domain = $domain -replace "^https?://", ""
$domain = $domain.TrimEnd("/")

if (-not $domain) {
    Write-Host "No domain entered." -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path (Join-Path $Root "data") | Out-Null
$domain | Out-File -FilePath $domainFile -Encoding utf8 -NoNewline

Write-Host ""
Write-Host "Permanent domain saved: https://$domain/" -ForegroundColor Green
Write-Host "Starting the website with that address..."
Write-Host ""

& (Join-Path $Root "start-public.ps1")
