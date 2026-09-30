$timeout = 240
$elapsed = 0
Write-Host "In attesa che la repository 'plumbline' venga creata su GitHub..." -ForegroundColor Cyan

while ($elapsed -lt $timeout) {
    git ls-remote origin *>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository rilevata su GitHub! Esecuzione di git push..." -ForegroundColor Green
        git push -u origin master
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PUSH COMPLETATO CON SUCCESSO!" -ForegroundColor Green
            Write-Host "Repository online su: https://github.com/mareknardella-lgtm/plumbline" -ForegroundColor Green
        } else {
            Write-Host "Errore durante il git push. Controlla le credenziali." -ForegroundColor Red
        }
        exit 0
    }
    Start-Sleep -Seconds 5
    $elapsed += 5
}

Write-Host "Timeout: repository non ancora rilevata. Puoi riprovare eseguendo .\scripts\publish.ps1" -ForegroundColor Yellow
exit 1
