# Plumbline one-click GitHub push script
Write-Host "Checking GitHub remote https://github.com/mareknardella-lgtm/plumbline.git..." -ForegroundColor Cyan

$remoteExists = $false
try {
    git ls-remote origin 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $remoteExists = $true
    }
} catch {
    $remoteExists = $false
}

if (-not $remoteExists) {
    Write-Host "Repository 'plumbline' not found on GitHub yet." -ForegroundColor Yellow
    Write-Host "Please create it at: https://github.com/new" -ForegroundColor Yellow
    Write-Host "Name: plumbline" -ForegroundColor Yellow
    Write-Host "Visibility: Public" -ForegroundColor Yellow
    Write-Host "Do NOT initialize with README, .gitignore or license." -ForegroundColor Yellow
    Write-Host ""
    $prompt = Read-Host "Once created, press Enter to push (or 'q' to quit)"
    if ($prompt -eq 'q') {
        exit 0
    }
}

Write-Host "Pushing commits and tags to origin master..." -ForegroundColor Green
git push -u origin master

if ($LASTEXITCODE -eq 0) {
    Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repo URL: https://github.com/mareknardella-lgtm/plumbline" -ForegroundColor Green
} else {
    Write-Host "Push failed. Please check your GitHub credentials or permissions." -ForegroundColor Red
}
