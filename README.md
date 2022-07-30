# FastAPI auth template
This project is a FastAPI REST API template with authentication and authorization. This API is using a MongoDB instance to store and retrive data.

# General informations
In this sections the general informations about the project are presented.

## Scripts
Some scripts are available in the ```scripts/``` directory they have different purposes:
- ```init.sh``` will check the project directory integrity and then create a ```.env``` file in the project root to then export the newly generated environement variables.
- ```serve_dev.sh``` will run a uvicorn server in dev mode with reload detection.
- ```test.sh``` will install locally the src package contained inside the ```$(pwd)/api/``` directory to the be able to run the pytest tests contained inside the ```$(pwd)/tests/``` directory.

## Start-up
To configure the develpement environement 2 scenarios may come up:
- It is the first time you fire up the project
- You already run and started developing over this project.

If you are in the first case you may want to run a script that checks if the directory is correctly configured and all the pieces are at their place, so run the ```init.sh``` script by typing ```$ chmod 777 ./scripts/init.sh && ./scripts/init.sh``` in your shell. This command will do some checks on the directories and export the required environement variables for the project to run.

Otherwise is not the first time you launch this project you will just need to export the environement variables with the ```.env``` file generated w/ ```init.sh``` script by typing ```$ set -a; source PATH TO DOTENV; set +a```.

Whenever you are ready to try the api simpy run the ```serve_dev.sh``` script by typing ```$ chmod 777 ./scripts/serve_dev.sh && ./scripts/serve_dev.sh``` which will start an uvicorn instance.

## Testing
To run the available tests inside ```$(pwd)/tests/``` run from your shell:
```
    $ chmod 777 ./scripts/test.sh && ./scripts/test.sh
```

which will make the script executable and then perform the action described at [this section](#scripts).