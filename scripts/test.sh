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

pip install -e ..