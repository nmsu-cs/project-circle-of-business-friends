$frontend = Get-Item -Path ".\frontend/NMSUandMe" | Resolve-Path

$frontendCommand1 = "npm install"
$frontendCommand2 = "yarn install"

Start-Process powershell -ArgumentList  "-Command", "cd '$frontend'; $frontendCommand1; $frontendCommand2"
