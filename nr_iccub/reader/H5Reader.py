import h5py

class H5Reader:
    """
    Parent class for h5 reader class. Do not instiantiate
    """
    def __init__(self, path):
        self.path = path
        self.file = h5py.File(self.path,'r')
        self.modes_in_file = ""
        self.psi4 = ""
        self.strain = ""
