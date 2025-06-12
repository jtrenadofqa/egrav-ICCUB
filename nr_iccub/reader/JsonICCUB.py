import json

class JsonICCUB():
    '''
    Reader class for ICCUB json files.

    Args:
        json_path (str): path to the simulation json file 
            containing the simulation's metadata. 

    Attributes:
        file (str): path to file 
        metadata (dict): dictionary with the metadata 
    '''

    def __init__(self, json_path):
        self.file = json_path
        self.metadata = self.get_json()

    def get_json(self):
        '''
        Module which loads json files
        '''
        f = open(self.file)
        return json.load(f)

    