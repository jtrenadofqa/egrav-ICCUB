from nr_iccub.nr_post import gw_math

class NRsim:
    """
    Parent class for containers of ICCUB NR simulations.
    Note that each instance can contain several modes, but
    only one extraction radius (possibly equal to infty).

    Do not instantiate.

    Args:
        path (str): path to simulation folder
        list_modes (list): list of tumples of modes. Defaults to [(2,2)]
        rd (str): extraction radius. Defaults to "100.00"

    Attributes:
        path (str) : path to simulation folder
        list_modes (list): list of tuple modes to compute/extract
        radius_to_compute (str): extraction radius
        time (np.array): array with time values. This is the same for all modes
        psi4 (dict): dictionary with the modes of psi4. The keys are the lms
        hdot (dict): dictionary with the modes of hdot. The keys are the lms.
        h (dict): dictionary with the modes of the strain h. The keys are the lms.
        adm_param (dict): dictionary with the metadata of the simulations, most importantly the
            ADM initial data

    """
    def __init__(self, path, list_modes=[(2,2)], rd = "100.00"):
        self.path = path
        self.list_modes = list_modes
        self.radius_to_compute = rd
        self.time = None
        self.psi4 = {}
        self.hdot = {}
        self.h = {}
        self.adm_param = None

    def check_modes(self, available_modes):
        '''
        Module which checks if the modes of interest (in self.list_modes) 
        are present in the list of available modes (found in the h5 file of 
        the simulation). If not all wanted modes are available raises a 
        SystemExit
        
        Args:
            available_modes (list): list of available modes
            
        Raises:
            SystemExit: If modes with which class was instatiated are not available in the data
        '''
        wanted_modes = self.list_modes
        bad_modes = []
        for lm in wanted_modes:
            if lm not in available_modes:
                bad_modes.append(lm)
        if len(bad_modes) == 0:
            return
        else:
            raise SystemExit(f"SystemExit: Modes {bad_modes} not available.\nPossible modes: {available_modes}")

    def check_radius(self, available_radii):
        '''
        Module which checks if the radius of interest (in self.radius_to_compute) 
        are present in the list of available radii (found in the h5 file of 
        the simulation). If the selected radius is available, it raises a 
        SystemExit
        
        Args:
            available_radii (list): list of available radii
            
        Raises:
            SystemExit: If radius with which class was instatiated is not available in the data
        '''
        wanted_r = self.radius_to_compute
        if wanted_r not in available_radii:
            raise SystemExit(f"SystemExit: radius {wanted_r} not available.\nPossible radii: {available_radii}")
        else:
            pass

    def compute_signals(self):
        """To implement in daughter classes"""
        raise NotImplementedError()

    def get_mode(self, mode, tp="h"):
        '''
        Module which outputs a standard signal based on the 
        selected modes and signal type

        Args:
            mode (tuple): lm of the mode of interest
            tp (str): type of signal, psi4, hdot or h. Defaults to h

        Raises:
            SystemExit: If selected signal type is not any of psi4, hdot or h
        '''
        if tp == "psi4":
            return gw_math.st_signal(self.time, self.psi4[mode])
        elif tp == "hdot":
            return gw_math.st_signal(self.time, self.hdot[mode])
        elif tp == "h":
            return gw_math.st_signal(self.time, self.h[mode])
        else:
            raise SystemExit(f"SystemExit: {tp} not available")


