$backend = Get-Item -Path ".\backend" | Resolve-Path
$frontend = Get-Item -Path ".\frontend/NMSUandMe" | Resolve-Path

$backendCommand = "flask run"
$frontendCommand = "yarn dev"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backend'; $backendCommand"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontend'; $frontendCommand"