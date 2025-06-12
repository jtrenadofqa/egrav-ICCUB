from nr_iccub.reader.H5ICCUB import H5ICCUB
from nr_iccub.reader.JsonICCUB import JsonICCUB

from nr_iccub.nr_post import gw_math
from nr_iccub.sim.NRsim import NRsim

class NRsim_from_ICCUB(NRsim):
    """
    Daughter class from NRsim that reads NR simulations from ICCUB's
    NR catalog.

    Args:
        path (str): path to simulation folder
        list_modes (list, optional): list of tumples of modes. Defaults to [(2,2)]
        rd (str, optional): extraction radius. Defaults to "100.00"
        f0 (float, optional): frequency cutoff for fixed frequency integration. Defaults to None
            If not provided, will attempt to read it from metadata. If provided, will use the
            provided value in all time integration 
        h_from_file (bool, optional): True for reading the h modes directly from the h5 data, 
            False for recomputing them from psi4. Defaults to True

    Attributes:
        h_from_file (bool) : True for reading the h modes directly from the h5 data, 
            False for recomputing them from psi4
        id (str): catalog ID of the simulation, read from simulation path
        h5 (H5ICCUB): h5 data with the waveforms
        time (np.array): array with time values. This is the same for all modes
        adm_param (dict): dictionary with the metadata of the simulations, most importantly the
            ADM initial data
    """
    def __init__(self, path, list_modes=[(2,2)], 
                            rd = "100.00",
                            f0 = None,
                            h_from_file = True):
        
        super().__init__(path, list_modes)
        self.radius_to_compute = rd
        self.h_from_file = h_from_file
        self.id = self.get_ID_from_path(path)

        self.h5 = self.read_h5wf() 
        self.adm_param = self.read_metadata()

        if f0 is None:
            f0_meta = self.adm_param['f0']
            self.f0 = f0_meta
            print(f'Using value of f0 in metadata, f0 = {self.f0:.4f}')
        else:
            self.f0 = f0
            print(f'Using value of f0 given, f0 = {self.f0:.4f}')

        self.compute_signals()
        
    def compute_signals(self):
        '''
        Reads psi4 from h5 data, and either reads or computes h depending on the parameter
        `h_from_file`. Computes the hdot waveforms with FFI from psi4. Loops through all the 
        modes included in `self.list_modes`

        Stores the results in the class attribute dictionaries psi4, hdot, h and the time array t.

        Raises:
            SystemExit if no value of f0 is declared
        '''
        
        for lm in self.list_modes:
            t, self.psi4[lm] = self.h5.read_data(kind = 'psi4', 
                                                 lm = lm, 
                                                 r = self.radius_to_compute)
            
            psi4_signal = gw_math.st_signal(t, self.psi4[lm])
            t, self.hdot[lm] = gw_math.ffi(psi4_signal, order = 1, f0 = self.f0)

            if self.h_from_file:
                t, self.h[lm] = self.h5.read_data(kind = 'h', 
                                                  lm = lm, 
                                                  r = self.radius_to_compute)
            else:
                if self.f0 is None:
                    raise SystemExit('FFI method requires specifying kwarg f0')
                else:
                    _, self.h[lm] = gw_math.ffi(psi4_signal, order = 2, f0 = self.f0)

        self.time = t

    def read_h5wf(self):
        '''
        Read h5 data and checks if the desired modes and radii ara available.
        '''
        h5_path = f'{self.path}/{self.id}_wf.h5'
        h5 = H5ICCUB(h5_path)

        modes_available = h5.get_modes()
        self.check_modes(modes_available)

        radii_available = h5.get_radii()
        self.check_radius(radii_available)

        return h5

    def read_metadata(self):
        '''
        Reads json metadata
        '''
        json_path = f'{self.path}/{self.id}_metadata.json'
        meta = JsonICCUB(json_path)
        return meta.get_json()

    def get_ID_from_path(self, path):
        '''
        Extracts the simulation ID from the simulations path
        '''
        id = path.split('/')[-2].split('ICCUB-')[-1]
        return id 
    
    