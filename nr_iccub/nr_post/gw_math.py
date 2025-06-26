'''
This module provides basic functionality to manipulate
the waveforms from the NR ICCUB catalog. 

The basic class is `st_signal`. When possible, all operations
are expressed in terms of this class.
'''


import collections
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq

####################################################
## ffi
####################################################

def fixed_freq_int_n(signal, f0, order = 2, dt = 1):
    """
    Low level module to perform fixed frequency 
    integration (FFI) in the time domain as proposed 
    by [paper] in terms of numpy arrays. 

    Args:
        signal (np.array): waveform to be integrated
        f0 (float): the cutoff frequency
        order (int): number of time integrations
        dt (float): the sampling of the signal

    Returns:
        np.array with the integrated signal
    """

    f = fftfreq( signal.shape[ 0 ], dt )

    idx_p = np.logical_and(f >= 0, f < f0)
    idx_m = np.logical_and(f <  0, f > -f0)

    f[idx_p] = f0
    f[idx_m] = -f0

    D0 = -1j/(2*np.pi*f)
    return ifft(D0**order * fft(signal))

def ffi(signal, order = 1, f0 = 0.01):
    ''' 
    Wrapper on `fixed_freq_int_n` which implements FFI

    Args:
        signal (st_signal): waveform to be integrated
        order (int, optional): number of time integrations. 
            Defaults to 1
        f0 (float, optional): the cutoff frequency. 
            Defaults to 0.01

    Returns:
        st_signal with the integrated signal
    '''
    dt = signal.time[1] - signal.time[0]
    result = fixed_freq_int_n(signal.value, f0, order = order, dt = dt)
    sgn_ffi = st_signal( signal.time, result )
    return sgn_ffi

####################################################
## extrapolate
####################################################

def extrap_psi4(psi4_signal, f0=None, r='100.00', lm=(2, 2), m0=1.):
    '''
    Module which implements the first order radius extrapolation 
    from a finite radius to infinity as proposed in [paper].
    In principle it can receive any standard signal, but the
    intended use is for a st_signal containing psi4 data

    Args:
        psi4_signal (st_signal): psi4 waveform to be integrated
        f0 (float, optional): cutoff frequency for FFI integration. 
            Defaults to 0.01
        r (str): radius of extraction, e.g. `167.00`. Kept as string since
            in most other places in the code these are expressed as str. 
            Defaults to `100.00`
        lm (tuple of int): tuple corresponding to the spherical harmonics of the mode.
            Defaults to (2,2)
        m0 (float, optional): total mass of the system. In all of our simulations 
            this is set to 1. Defaults to 1.

    Returns:
        st_signal with the extrapolated value
    '''

    hdot = ffi(psi4_signal, order = 1, f0=f0)

    l, m = lm
    r0 = float(r)
    rA = r0*(1. + m0/(2.*r0))**2
    C  = 1. - 2.*m0/rA
    return st_signal(psi4_signal.time, 
                     C*(psi4_signal.value - (l-1)*(l+2)/(2*rA)*hdot.value))

####################################################
## standard signal
####################################################

def st_signal(xdata, ydata):
    '''
    Standard class to use for nr signals

    Args:
        xdata (np.array): xdata to fill the time argument class
        ydata (np.array): ydata to fill the magnitude argument class

    Returns:
        namedtuple with the standard signal
    '''
    Signal = collections.namedtuple("Signal", "time value")
    signal = Signal(time=xdata, value=ydata)
    return signal