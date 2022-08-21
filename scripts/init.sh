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

# Useful variables.
LOCALHOST="localhost"
DOCKER_INTERNAL="host.docker.internal"

################################################################################
# Reading input arguments.
# Making sure the number read arguments is correct.
if [ "$#" -ne 1 -a "$#" -ne 3 ]; then
    echo "To generate a local development .env file simply type::"
    echo -e "${ORANGE}Usage: init.sh <configs-dir-absolute-path> <logging-dir-absolute-path> <dotenv-absolute-path>${NC}"
    echo 
    echo "To generate a container .env file type instead::"
    echo -e "${ORANGE}Usage: init.sh <dotenv-absolute-path>${NC}"
    echo
    echo "Interrupting."
    exit -1
fi

# Making sure the arguments are absolute paths.
if [ "$#" -eq 3 ]; then
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

    # if the validation is passed initialize all the variables.
    CONFIGS_DIR=$1
    LOGGING_DIR=$2
    DOTENV=$3
    DB_DEFAULT_HOST=$LOCALHOST
else
    if [[ ! "$1" = /* ]]; then
        echo -e "${RED}The dotenv file path must be absolute.${NC}"
        echo "Interrupting."
        exit -1
    fi

    CONFIGS_DIR="/app/configs"
    LOGGING_DIR="/app/logs"
    DOTENV=$1
    DB_DEFAULT_HOST=$DOCKER_INTERNAL
fi

################################################################################
# Variables initiaization.

SECRET_KEY=$(openssl rand -hex 32)
echo "Initializing workspace..."

################################################################################
# Dicrectories check.
if [ "$#" -eq 3 ]; then
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
fi

################################################################################
# DB connection setup.
echo "Insert DB connection username:: "
read DB_USERNAME

echo "Insert DB connection password:: "
read DB_PASSWORD

echo "If you are running the code on you local machine and talking with a DB on you local machine simply type $LOCALHOST"
echo "If you are running the code inside a container and talking with a DB on your local machine simly type $DOCKER_INTERNAL"
echo "If you are running the code with a docker docker compose simply type the name of the DB service in the docker compose as host"
echo "If you are running the code connecting it with a remode DB simply type the host of the remote server..."
echo "Insert DB connection host::"
read DB_HOST
# if [ -z $DB_HOST ]; then
#     DB_HOST=$DB_DEFAULT_HOST
# fi

echo "Insert DB connection port:: "
read DB_PORT

echo "Insert DB name:: "
read DB_NAME

################################################################################
# .env printing.

# Generating the env folder if not exists.
if [ ! -e "$(dirname $DOTENV)" ]; then
    echo -e "${ORANGE}$(dirname $DOTENV) does not exist, creating...${NC}"
    mkdir -p $(dirname $DOTENV)
    echo -e "Success, moving on..."
fi

# Printing variables to .env file.
echo "Printing required environement variables to $(pwd)/$DOTENV file..."
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
