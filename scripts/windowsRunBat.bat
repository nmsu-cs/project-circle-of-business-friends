@echo off

rem 
set "backend=.\backend"
set "frontend=.\frontend/NMSUandMe"

rem 
set "backendCommand=flask run"
set "frontendCommand=yarn dev"

rem 
start cmd.exe /k "cd /d "%backend%" && %backendCommand%"

rem 
start cmd.exe /k "cd /d "%frontend%" && %frontendCommand%"