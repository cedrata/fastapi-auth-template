#!/bin/bash

################################################################################
# This script will ONLY export the environement variables from the .env file.
# This scrtip assumes you already have a dotenv file.
# Currently this script runs under MacOS and Ubuntu-like distros (of course wsl
# ubuntu too :)).
# May not work for other distros.
################################################################################

################################################################################
# Echo text colors.
RED='\033[33;31m'
GREEN='\033[33;32m'
ORANGE='\033[33;33m'

################################################################################
# Reading input arguments.
# Making sure the number read arguments is correct.
if [ "$#" -lt 1 ]; then
    echo -e "${ORANGE}Usage: env.sh <dotenv-absolute-path>"
    echo "Interrupting."
    exit -1
fi

# Making sure the first argument is an absolute path.
if [[ ! "$1" = /* ]]; then
    echo -e "${RED}The dotenv path must be absolute."
    echo "Interrupting."
    exit -1
fi

################################################################################
# Variables initiaization.

# If the validation is passed initialize all the variables.
DOTENV=$1

# Different variables from input arguments.
ERROR=false

################################################################################
# Exporting variables to environement.
echo "Exporting variables to the environement..."
set -a
if [ ! -f $DOTENV ]; then
    echo -e "${RED}An error occured setting the variables, check that the ${DOTENV} file exists."
    ERROR=true
else
    echo "Environement variables exported with success."
fi
set +a

if [[ "$ERROR" = "true" ]]; then
    echo -e "${RED}Interrupting."
    exit -2
fi

echo -e "${GREEN}Success, you're ready to work :)"
exit 0