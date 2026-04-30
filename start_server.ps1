$ErrorActionPreference = "Stop"
$projectPath = "c:\Users\HP\OneDrive\Documents\new project election"
$venvPip = Join-Path $projectPath "venv\Scripts\pip.exe"
$venvPython = Join-Path $projectPath "venv\Scripts\python.exe"
$managePy = Join-Path $projectPath "manage.py"
$reqFile = Join-Path $projectPath "requirements.txt"

Write-Host "Installing dependencies..." -ForegroundColor Cyan
& $venvPip install -r $reqFile

Write-Host "`nRunning migrations..." -ForegroundColor Cyan
& $venvPython $managePy migrate

Write-Host "`nStarting Django server at http://127.0.0.1:8000" -ForegroundColor Green
& $venvPython $managePy runserver 127.0.0.1:8000
