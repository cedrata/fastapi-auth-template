#!/bin/bash

################################################################################
# This script will run the setup to install, for development, the src module
# contained inside the $(pwd)/../api directory. 
# This operation is required in orer to run tests in the 
# $(pwd)/../tests directory.
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
if [ "$#" -lt 1 ]; then
    echo -e "${ORANGE}Usage: test.sh <module-directory-absolute-path>"
    echo "Interrupting."
    exit -1
fi

# Making sure the arguments are absolute paths.
if [[ ! "$1" = /* ]]; then
    echo -e "${RED}The module-directory path must be absolute."
    echo "Interrupting."
    exit -1
elif [ ! -d "$1" ]; then
    echo -e "${RED}The module-directory path does not exists."
    echo "Interrupting."
    exit -1
fi

################################################################################
# Variables initiaization.

# if the validation is passed initialize all the variables.
MODULE_DIR=$1


################################################################################
# Executing the command.
pip install -e $MODULE_DIR