@echo off

rem Define the paths to the directories
set "backend=.\backend"
set "frontend=.\frontend/NMSUandMe"

rem Define the commands to be executed in each directory
set "backendCommand=flask run"
set "frontendCommand=yarn dev"

rem Open a new command prompt window and execute command 1
start cmd.exe /k "cd /d "%backend%" && %backendCommand%"

rem Open another new command prompt window and execute command 2
start cmd.exe /k "cd /d "%frontend%" && %frontendCommand%"