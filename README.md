# FastAPI auth template
This project is a FastAPI REST API template with authentication and authorization. This API is using a MongoDB instance to store and retrive data.

# General informations
In this sections the general informations about the project are presented.

## Scripts
Some scripts are available in the ```scripts/``` directory they have different purposes:
- ```freeze.sh``` will execute the ```pip freeze``` command but excluding local modules generated with ```test.sh```.
- ```init.sh``` will check the project directory integrity and then create a ```.env``` file in the project root to then export the newly generated environement variables.
- ```serve_dev.sh``` will run a uvicorn server in dev mode with reload detection. (If you are using visual studio code you can run add a configuration to run in debug mode the FastAPI application, just so you know, to simplify the development).
- ```test.sh``` will install locally the src package contained inside the ```$(pwd)/api/``` directory to the be able to run the pytest tests contained inside the ```$(pwd)/tests/``` directory.

## Initialization
To run the application some environement variables are required, it is possible to generate them via the ```init.sh``` script. You can simply type from the root of the repository ```$ chmod 777 ./scripts/init.sh && ./scripts/init.sh``` to launch the script. Arguments are required to run the script, the last one will be a ".env" file an absolute file path is required, it is not mandatory that it's an existing file because it will be generated if required.\
The following naming convention has been decided:
- ```.dev.env``` for the developement environement.
- ```.test.env``` for the test environement (the only difference now are the variables for the DB connection like port, host and so on).


## Start-up
The application is not containerized right now (it soon will), and to startup the developement environement 2 options are available:
- Run from terminal
- Run from IDE

To run the application via terminal the ```serve_dev.sh``` script is available, simply execute it with ```$ chmod 777 ./scripts/serve_dev.sh && ./scripts/serve_dev.sh absolute/path/to/.dev.env```

Otherwise if you're using VsCode (I know it's not an IDE but a text editor really close to a IDE if customized), in the debug configuration you can add a new configuration for python programs, then a new menu is displayed where to chose the "FastAPI" application. A json file will be displayed, insert the following body, if required adapt it
```json
{ 
    "name": "Python: FastAPI DEV",
    "type": "python",
    "request": "launch",
    "module": "uvicorn",
    "args": [
        "src.app:fastapi_app",
        "--reload"
    ],
    "jinja": true,
    "justMyCode": false,
    "envFile": "${workspaceFolder}/env/.dev.env"
}
```

by doing so yow will be able to run and insert debug points into the application and debug it visually.

## Testing
To run the available unit tests inside ```$(pwd)/tests/``` run from your shell:
```
    $ chmod 777 ./scripts/test.sh && ./scripts/test.sh $(pwd)
```
This will install locally the ```src``` module inside the ```api``` directory.

which will make the script executable and then perform the action described at [this section](#scripts).

To then execute the tests you can either run them from you IDE (VsCode in my case) or terminal with ```pytest --envfile=$(pwd)/env/.test.env``` this flag exists because of the ```pytest-dotenv``` plugin for pytest present in the requirements.txt file.