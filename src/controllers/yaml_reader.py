import yaml
import os

class YamlReader:
    """
    Processing the yaml file
    -------
    locates yaml file from parsed CLI command within current working directory
    loads yaml file data to use for presenting the 3D model
    """
    def read_file(self, file):
        print(file)
        current_working_directory = str(os.getcwd())
        openfile = os.path.join(current_working_directory, file)
        with open(openfile, "r") as file:
            input_file = yaml.safe_load(file)
        return input_file
