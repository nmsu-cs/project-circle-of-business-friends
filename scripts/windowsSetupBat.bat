@echo off

rem 
set "frontend=.\frontend\NMSUandMe"

rem
set "frontendCommand1=npm install"
set "frontendCommand2=yarn install"

rem
cd /d "%frontend%" && %frontendCommand1% && %frontendCommand2%