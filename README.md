# Python-API
![CI](https://github.com/Crop-Simulator/Python-API/actions/workflows/release-build.yml/badge.svg)

## Launch API
Use the following command to run the code
```commandline
python src/launch.py data.yml
```
## Install
### Python Version
The build is tested on [Python 3.10.2](https://www.python.org/downloads/release/python-3102/) and is our recommended Python version.

### Build Setup
Use the following command to install the packages according to the requirements file
```commandline
pip install -r requirements.txt
```
### Installing Blender
To install Blender following [these instructions](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html). 
The build is tested on Blender 3.5 and is our recommended version.

### Updating Requirements.txt
To update requirements.txt install [pipreqs](https://github.com/bndr/pipreqs)
```commandline
pip install pipreqs
```
Then use the following command in the root folder
```commandline
pipreqs --force 
```
## Linting
To lint the code install [ruff](https://github.com/astral-sh/ruff)
```commandline
pip install ruff
```
Then use the following command to run Ruff over the project
```commandline
ruff check .
```
If Ruff considers an error "fixable" it can be resolved by running the following
```commandline
ruff check --fix .
```


## Testing
To run the all the unit tests use the following command from the root directory of your checkout
```commandline
python -m unittest
```

To run a single unit test file use 
```commandline
python -m unittest tests/test_launch.py
```