#!/bin/bash

################################################################################
# This script will run the setup to prepare the develpment environment, and 
# export them.
# Currently this script runs under MacOS and Ubuntu-like distros (of course wsl
# ubuntu too :)).
# May not work for other distros.
################################################################################

################################################################################
# Variables initiaization.

# Echo text colors.
DEFAULT_COLOUR='\033[33;0m'
RED='\033[33;31m'
GREEN='\033[33;32m'
ORANGE='\033[33;33m'

# Environement variabled.
SECRET_KEY=$(openssl rand -hex 32)
CONFIGS_DIR=$(pwd)/../configs
LOGGING_DIR=$(pwd)/../logs

# File containing the environement variables to export.
DOTENV=$(pwd)/../.env

echo -e "${DEFAULT_COLOUR}Initializing workspace..."

################################################################################
# Dicrectories check.
echo "Check if logging directory is already present..."
if [ ! -d $LOGGING_DIR ]; then
    mkdir $LOGGING_DIR
    echo -e "${GREEN}Loggin directory was missing, generated with success."
else
    echo -e "${DEFAULT_COLOUR}Loggin directory already existing, moving on..."
fi

if [ ! -d $CONFIGS_DIR ]; then
    echo -e "${ORANGE}The $CONFIGS_DIR is missing, create it or check the name is typed correctly..."
else
    echo -e "${DEFAULT_COLOUR}Configuration directory existing, moving on..."
fi
echo -e "${DEFAULT_COLOUR}Dicrectories validated with success."

################################################################################
# Printing variables to .env file.
echo "Printing required environement variables to $(pwd)/.env file..."
echo "SECRET_KEY=${SECRET_KEY}" > $DOTENV
echo "CONFIGS_DIR=${CONFIGS_DIR}" >> $DOTENV
echo "LOGGING_DIR=${LOGGING_DIR}" >> $DOTENV
echo "${DOTENV} file created succesfully."


################################################################################
# Exporting variables to environement.
echo "Exporting variables to the environement..."
set -a
source "${DOTENV}"
set +a
echo "Environement variables exported with success."

echo -e "${GREEN}Success, you're ready to work :)"
exit 0