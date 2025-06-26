import numpy as np
import pandas as pd

from nr_iccub.reader.H5Reader import H5Reader

class H5ICCUB(H5Reader):
    '''
    Reader class for ICCUB h5 files.

    Args:
        h5_path (str): path to the simulation h5 file.

    Attributes:
        modes_in_file (list): 
        radii_in_file (list): 
    '''
    def __init__(self, h5_path):
        super().__init__(h5_path)
        self.modes_in_file = self.get_modes()
        self.radii_in_file = self.get_radii()

    def get_modes(self):
        '''
        Module which finds the list of lm modes available
        in the h5 file

        Returns:
            list of lm modes each of which is a tuple of 2 ints
        '''
        modes=[]
        for key in self.file.keys():
            if "h" in key:
                l = int(key.split("_")[1][1:])
                m = int(key.split("_")[2][1:])
                r = key.split("_r")[1]
                modes.append((l,m))
        return list(pd.Series(modes).unique())
    
    def get_radii(self):
        '''
        Module which finds the list of radii available
        in the h5 file

        Returns:
            list of radii each of which is a string
        '''
        radii = []
        for key in self.file.keys():
            if "h" in key:
                r = key.split("_r")[1]
                radii.append(r)
        return list(pd.Series(radii).unique())

    def read_data(self, kind = 'h', lm = (2,2), r = '100.00'):
       '''
        Module which reads the signal data from the h5 file

        Args:
            kind (str): type of signal to read, valid options 
                are h or psi4. Defaults to h
            lm (tuple): mode of interest. Defaults to (2,2)
            r (str): radius of extraction. Could be `extrap` for extrapolated
                signal. Defaults to '100.00'
  
        Returns:
            tuple of numpy arrays with the time and waveform values
        '''
       l, m = lm
       key=f'{kind}_l{l}_m{m}_r{r}'
       t_key=f't_r{r}'
       return np.array(self.file[t_key]), np.array(self.file[key]) 

