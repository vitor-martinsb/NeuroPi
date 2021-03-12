import numpy as np
import sys

def filter_car(signal,n_electrodes):
    
    sig_ac=signal.sum(axis=1, dtype='float')
    Dim=float(np.shape(signal))
    L=Dim[1]
    C=Dim[2]
    signal_car=np.zeros([L,C])
    
    aux=1/n_electrodes
    for elec in range(0,n_electrodes-1):
        signal_car[:,elec]=signal[:,elec]-aux*sig_ac
        
    return signal_car
    