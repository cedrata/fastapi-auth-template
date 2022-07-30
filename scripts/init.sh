#!/bin/bash

################################################################################
# This script will run the setup to prepare the develpment environment, and 
# export them.
# Currently this script runs under MacOS and Ubuntu-like distros (of course wsl
# ubuntu too :)).
# May not work for other distros.
################################################################################

################################################################################
# Echo text colors.
DEFAULT_COLOUR='\033[33;0m'
RED='\033[33;31m'
GREEN='\033[33;32m'
ORANGE='\033[33;33m'

################################################################################
# Reading input arguments.
# Making sure the number read arguments is correct.
if [ "$#" -lt 3 ]; then
    echo -e "${ORANGE}Usage: env.sh <configs-dir-absolute-path> <logging-dir-absolute-path> <dotenv-absolute-path>"
    echo "Interrupting."
    return -1
fi

# Making sure the arguments are absolute paths.
if [[ ! "$1" = /* ]]; then
    echo -e "${RED}The configs directory path must be absolute or does not exists."
    echo "Interrupting."
    exit -1
elif [[ ! "$2" = /* ]]; then
    echo -e "${RED}The logging directory must be absolute or does not exists."
    echo "Interrupting."
    exit -1
elif [[ ! "$3" = /* ]]; then
    echo -e "${RED}The dotenv path must be absolute or does not exists."
    echo "Interrupting."
    exit -1
fi

################################################################################
# Variables initiaization.

# if the validation is passed initialize all the variables.
CONFIGS_DIR=$1
LOGGING_DIR=$2
DOTENV=$3

# Differnt variables from input arguments.
SECRET_KEY=$(openssl rand -hex 32)
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
echo -e "${GREEN}Dicrectories validated with success."
echo -e "${DEFAULT_COLOUR}"

################################################################################
# Printing variables to .env file.
echo "Printing required environement variables to $(pwd)/.env file..."
echo "SECRET_KEY=${SECRET_KEY}" > $DOTENV
echo "CONFIGS_DIR=${CONFIGS_DIR}" >> $DOTENV
echo "LOGGING_DIR=${LOGGING_DIR}" >> $DOTENV
echo -e "${GREEN}$DOTENV file created succesfully."
echo -e "${DEFAULT_COLOUR} Now you can execute the following command to set the environement variables: " 
echo ""
echo -e "\tenv" '$(cat PATH TO DOTENV | xargs)'
echo ""

echo -e "${GREEN}Success, you're ready to work :)"