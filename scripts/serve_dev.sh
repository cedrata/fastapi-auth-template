#!/bin/bash

################################################################################
# This script will run the command to launch the uvicorn server for out api.
# Currently this script runs under MacOS and Ubuntu-like distros (of course wsl
# ubuntu too :)).
# May not work for other distros.
# UPDATE: On my machine running WSL2 I was facing a tedious issue.
# After generating the .env file content to environement variables and running
# the dev server with uvicorn the environement variables were not seen by the 
# python application, so an flag is added in this simple script, absolute .env
# file path, so that uvicorn can run the application with those env variables.
################################################################################

# Syntax:
# src -> the module name.
# app -> submodule name containing the FastAPI instance.
# fastapi_app -> FastAPI instance.
# --env-file -> dotenv absolute file path.
# --realod -> uvicorn argument that detects when a file is changed in src module.

################################################################################
# Echo text colors.
DEFAULT_COLOUR='\033[33;0m'
RED='\033[33;31m'
GREEN='\033[33;32m'
ORANGE='\033[33;33m'


################################################################################
# Reading input arguments.
# Making sure the number read arguments is correct.
if [ "$#" -lt 1 ]; then
    echo -e "${ORANGE}Usage: serve_dev.sh <dotenv-absolute-path>"
    echo "Interrupting."
    exit -1
fi

# Making sure the arguments are absolute paths.
if [[ ! "$1" = /* ]]; then
    echo -e "${RED}The dotenv path path must be absolute or does not exists."
    echo "Interrupting."
    exit -1
fi

################################################################################
# Variables initiaization.

# if the validation is passed initialize all the variables.
DOTENV=$1

################################################################################
# Executing the command.
uvicorn src.app:fastapi_app --env-file $DOTENV --reload