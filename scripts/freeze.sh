#!/bin/bash

################################################################################
# This script will seimplify the operation of updating the requirements of 
# currently active pip environement.
# To prevent storing the test src module instalation, which is creating issues during
# the pip install -r operation, this script has been written.
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
    echo -e "${ORANGE}Usage: serve_dev.sh <requirements-path>"
    echo "Interrupting."
    exit -1
fi

################################################################################
# Variables initiaization.

# if the validation is passed initialize all the variables.
REQUIREMENTS=$1

################################################################################
# Executing the command.
pip freeze | grep -v "-e git" > $REQUIREMENTS