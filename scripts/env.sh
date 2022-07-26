#!/bin/bash

################################################################################
# This script will ONLY export the environement variables from the .env file.
# This scrtip assumes you already have a dotenv file.
# Currently this script runs under MacOS and Ubuntu-like distros (of course wsl
# ubuntu too :)).
# May not work for other distros.
################################################################################

################################################################################
# Variables initiaization.
# Echo text colors
RED='\033[33;31m'
GREEN='\033[33;32m'

DOTENV=$(pwd)/../.env

ERROR=false

################################################################################
# Exporting variables to environement.
echo "Exporting variables to the environement..."
set -a
if [ ! -f $DOTENV ]; then
    echo "${RED}An error occured setting the variables, check that the ${DOTENV} file exists."
    ERROR=true
else
    echo "Environement variables exported with success."
fi
set +a

if [[ "$ERROR" = "true" ]]; then
    echo -e "${RED}Interrupting."
    exit -1
fi

echo -e "${GREEN}Success, you're ready to work :)"
exit 0