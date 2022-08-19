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
NC='\033[33;0m'
RED='\033[33;31m'
GREEN='\033[33;32m'
ORANGE='\033[33;33m'

################################################################################
# Reading input arguments.
# Making sure the number read arguments is correct.
if [ "$#" -lt 3 ]; then
    echo -e "${ORANGE}Usage: env.sh <configs-dir-absolute-path> <logging-dir-absolute-path> <dotenv-absolute-path>${NC}"
    echo "Interrupting."
    exit -1
fi

# Making sure the arguments are absolute paths.
if [[ ! "$1" = /* ]]; then
    echo -e "${RED}The configs directory path must be absolute.${NC}"
    echo "Interrupting."
    exit -1
elif [ ! -d "$1" ]; then
    echo -e "${RED}The configs directory path does not exists.${NC}"
    echo "Interrupting."
    exit -1
elif [[ ! "$2" = /* ]]; then
    echo -e "${RED}The logging directory path must be absolute.${NC}"
    echo "Interrupting."
    exit -1
elif [ ! -d "$2" ]; then
    echo -e "${RED}The logging directory path does not exists.${NC}"
    echo "Interrupting."
    exit -1
elif [[ ! "$3" = /* ]]; then
    echo -e "${RED}The dotenv file path must be absolute.${NC}"
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
echo "Initializing workspace..."

################################################################################
# Dicrectories check.
echo "Check if logging directory is already present..."
if [ ! -d $LOGGING_DIR ]; then
    mkdir $LOGGING_DIR
    echo -e "${GREEN}Loggin directory was missing, generated with success.${NC}"
else
    echo "Loggin directory already existing, moving on..."
fi

if [ ! -d $CONFIGS_DIR ]; then
    echo -e "${ORANGE}The $CONFIGS_DIR is missing, create it or check the name is typed correctly...${NC}"
else
    echo "Configuration directory existing, moving on..."
fi
echo -e "${GREEN}Dicrectories validated with success.${NC}"

################################################################################
# DB connection setup.
echo "Insert DB connection username:: "
read DB_USERNAME

echo "Insert DB connection password:: "
read DB_PASSWORD

echo "Insert DB connection host:: "
read DB_HOST

echo "Insert DB connection port:: "
read DB_PORT

echo "Insert DB name:: "
read DB_NAME

################################################################################
# .env printing.

# Generating the env folder if not exists.
if [ ! -e "$(dirname $3)" ]; then
    echo -e "${ORANGE}$(dirname $3) does not exist, creating...${NC}"
    mkdir -p $(dirname $3)
    echo -e "Success, moving on..."
fi

# Printing variables to .env file.
echo "Printing required environement variables to $(pwd)/.env file..."
echo "SECRET_KEY=${SECRET_KEY}" >$DOTENV
echo "CONFIGS_DIR=${CONFIGS_DIR}" >>$DOTENV
echo "LOGGING_DIR=${LOGGING_DIR}" >>$DOTENV
echo "DB_USERNAME=${DB_USERNAME}" >>$DOTENV
echo "DB_PASSWORD=${DB_PASSWORD}" >>$DOTENV
echo "DB_HOST=${DB_HOST}" >>$DOTENV
echo "DB_PORT=${DB_PORT}" >>$DOTENV
echo "DB_NAME=${DB_NAME}" >>$DOTENV
echo -e "${GREEN}$DOTENV file created succesfully.${NC}"

echo -e "${GREEN}Success, you're ready to work :)${NC}"
