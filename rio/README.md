# 1721-ReefScape

## setup

You can enter a pipenv shell with

``` sh
pipenv shell
```

so you don't have to prefix every command with pipenv run

### local

make sure you have pipenv installed

create/update venv

``` sh
pipenv install
```

run simulator:

``` sh
pipenv run make sim
```

run tests:

``` sh
pipenv run make test
```

### robot

while connected to internet:

``` sh
pipenv run make sync # Sync robotpy requirements
pipenv run make download-python # Download python to computer for robot
```

after connecting to the robot:

``` sh
pipenv run make install-python # Install python to the robot
```

deploy code to the robot:

``` sh
pipenv run make deploy # Deploy only
pipenv run make nc # Deploy and open net console
pipenv run make rush # Deploy and open net console, skip tests and skip pushing new dependencies
```

You only have to run `make sync` when dependencies change in pyproject.toml
You only have to run `make download-python`, `make install-python` if the python version changes.
