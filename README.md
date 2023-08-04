# Python-API
![CI](https://github.com/Crop-Simulator/Python-API/actions/workflows/release-build.yml/badge.svg)

## Install
### Python Version
The build is tested on [Python 3.10.2](https://www.python.org/downloads/release/python-3102/) and is our recommended Python version.
We use [pyenv](https://github.com/pyenv/pyenv) to manage our Python versions and [Poetry](https://python-poetry.org/) to manage our packages and dependencies.  

### Pyenv Setup
- For UNIX/macOS, follow [these instructions](https://github.com/pyenv/pyenv#installation) to set up pyenv locally.
- For Windows, we recommend using the officially endorsed [pyenv fork](https://github.com/pyenv-win/pyenv-win#installation). 

Once installed, use the following command in commandline to install the supported Python version.
```commandline
pyenv install 3.10.2
```
After the Python version has been installed, type `pyenv local` and ensure the output is 3.10.2

### Poetry Setup
After installing the pyenv, install 
poetry using the [official instructions](https://python-poetry.org/docs/#installation).

#### Activating the virtual environment
Once poetry is installed, type the following to activate the virtual environment:
```commandline
poetry shell
```
To deactivate the venv and exit this new shell type `exit`

### Dependency Installation
While in the active venv, use the following command to install the dependencies.
```commandline
poetry install
```
#### Managing Dependencies
To add a new dependency use `poetry add <dependency name>`
- For more guidance on dependency management refer to poetry's [official website](https://python-poetry.org/docs/managing-dependencies/).

### Launch API
While in the active venv, use the following command to run the code
```commandline
poetry run python .\src\launch.py .\data.yml
```

### Installing Blender
To install Blender following [these instructions](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html). 
The build is tested on Blender 3.5 and is our recommended version.

## Linting
To lint the code we use [ruff](https://github.com/astral-sh/ruff). 
Use the following command to run Ruff over the project
```commandline
ruff check .
```
If Ruff considers an error "fixable" it can be resolved by running the following
```commandline
ruff check --fix .
```

## Testing
While in the active venv, to run the all the unit tests use the following command from the root directory of your checkout
```commandline
poetry run pytest 
```

To run a single unit test file use 
```commandline
poetry run pytest tests/test_launch.py
```