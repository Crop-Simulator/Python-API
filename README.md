# Python-API

## Install
Use the following command to install the packages according to the requirements file
```commandline
pip install -r requirements.txt
```
### Updating Requirements.txt
To update requirements.txt install [pipreqs](https://github.com/bndr/pipreqs)
```commandline
pip install pipreqs
```
Then use the following command in the root folder
```commandline
pipreqs --force 
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