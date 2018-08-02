import json
import os

module_dir = os.path.dirname(__file__)

class PConfig(object):

    def __init__(self, filepath):
        self.file = filepath
        self.__readfile()
        self.__validate()
    
    def __readfile(self):
        file_path = os.path.join(module_dir, self.file)

        with open(file_path) as f:
            config = json.load(f)
        
        assert ('tasks' in config), "The config file must be start with 'tasks'"
        self.tasks = config['tasks']
        self.output_folder = config['output_folder']

    def __validate(self):
        #todo: to validate the others values
        return True