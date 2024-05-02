#!/bin/bash

frontend=$(realpath "./frontend/NMSUandMe")

frontendCommand1="npm install"
frontendCommand2="yarn install"

cd "$frontend" && $frontendCommand1 && $frontendCommand2