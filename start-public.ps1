$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Test-Flask {
    try {
        $null = Invoke-WebRequest -Uri "http://127.0.0.1:5500/api/health" -UseBasicParsing -TimeoutSec 2
        return $true
    } catch {
        return $false
    }
}

function Save-Links($publicUrl) {
    $publicUrl = $publicUrl.TrimEnd("/")
    $publicUrl | Out-File -FilePath (Join-Path $Root "data\public-url.txt") -Encoding utf8 -NoNewline
    $links = @"
Geetha Gold Works - Public Links
================================

Website: $publicUrl/
Admin:   $publicUrl/admin

Login: admin / geetha123

IMPORTANT
- Keep this computer ON while the website is public.
- This address stays the same after restarts if you used setup-permanent-link.bat.
"@
    $links | Out-File -FilePath (Join-Path $Root "PUBLIC-LINKS.txt") -Encoding utf8
    Write-Host ""
    Write-Host $links -ForegroundColor Green
    Write-Host "Links saved to PUBLIC-LINKS.txt" -ForegroundColor Cyan
    Start-Process "$publicUrl/"
}

Write-Host ""
Write-Host "Geetha Gold Works - Starting public website..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Flask)) {
    Write-Host "Starting website server..."
    Start-Process python -ArgumentList "app.py" -WorkingDirectory $Root -WindowStyle Minimized
    for ($i = 0; $i -lt 20; $i++) {
        Start-Sleep -Seconds 1
        if (Test-Flask) { break }
    }
    if (-not (Test-Flask)) {
        Write-Host "Could not start website server." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Website server is running."

Get-CimInstance Win32_Process -Filter "Name = 'cloudflared.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*127.0.0.1:5500*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Get-Process ngrok -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

$domainFile = Join-Path $Root "data\permanent-domain.txt"
$permanentDomain = $null
if (Test-Path $domainFile) {
    $permanentDomain = (Get-Content $domainFile -Raw).Trim()
    $permanentDomain = $permanentDomain -replace "^https?://", ""
    $permanentDomain = $permanentDomain.TrimEnd("/")
}

if ($permanentDomain) {
    Write-Host "Starting permanent public link: https://$permanentDomain/"
    $logFile = Join-Path $Root "ngrok.log"
    if (Test-Path $logFile) { Remove-Item $logFile -Force }
    Start-Process -FilePath (Join-Path $Root "ngrok.exe") `
        -ArgumentList "http", "--url=$permanentDomain", "5500", "--log=stdout" `
        -RedirectStandardOutput $logFile `
        -WindowStyle Minimized | Out-Null

    $ready = $false
    for ($i = 0; $i -lt 40; $i++) {
        Start-Sleep -Seconds 1
        try {
            $null = Invoke-WebRequest -Uri "http://127.0.0.1:4040/api/tunnels" -UseBasicParsing -TimeoutSec 2
            $ready = $true
            break
        } catch {}
    }

    if ($ready) {
        Save-Links "https://$permanentDomain"
        exit 0
    }

    Write-Host "Permanent link did not start. Check ngrok.log. You may need to run setup-permanent-link.bat again." -ForegroundColor Yellow
    exit 1
}

Write-Host "No permanent domain yet. Using a temporary Cloudflare link."
Write-Host "To make a link that never changes, double-click setup-permanent-link.bat" -ForegroundColor Yellow

$logFile = Join-Path $Root "tunnel.log"
if (Test-Path $logFile) { Remove-Item $logFile -Force }

Start-Process -FilePath "$Root\cloudflared.exe" `
    -ArgumentList "tunnel", "--url", "http://127.0.0.1:5500", "--protocol", "http2" `
    -RedirectStandardError $logFile `
    -WindowStyle Minimized | Out-Null

$publicUrl = $null
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 1
    if (-not (Test-Path $logFile)) { continue }
    $content = Get-Content $logFile -Raw -ErrorAction SilentlyContinue
    if ($content -match "(https://[a-z0-9-]+\.trycloudflare\.com)") {
        $publicUrl = $Matches[1]
        break
    }
}

if (-not $publicUrl) {
    Write-Host "Public link is still starting. Check tunnel.log in a minute." -ForegroundColor Yellow
    exit 0
}

Save-Links $publicUrl
