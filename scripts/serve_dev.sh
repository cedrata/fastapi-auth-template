#!/bin/bash

################################################################################
# This script will run the command to launch the uvicorn server for out api.
# Currently this script runs under MacOS and Ubuntu-like distros (of course wsl
# ubuntu too :)).
# May not work for other distros.
################################################################################

# Syntax:
# src -> the module name.
# app -> submodule name containing the FastAPI instance.
# fastapi_app -> FastAPI instance.
# --realod -> uvicorn argument that detects when a file is changed in src module.
uvicorn src.app:fastapi_app --reload