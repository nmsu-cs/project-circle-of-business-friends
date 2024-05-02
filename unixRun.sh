#!/bin/bash

backend=$(realpath "./backend")
frontend=$(realpath "./frontend/NMSUandMe")

backendCommand="flask run"
frontendCommand="yarn dev"

cd "$backend" && $backendCommand &
cd "$frontend" && $frontendCommand &