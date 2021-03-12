import numpy as np

def car_filter(signal,n_electrodes,t_collect,fs):
    signal=signal[:,0:n_electrodes]
    sig_ac=signal.sum(axis=1, dtype='float')
    signal_car=np.zeros([int(t_collect*fs),int(n_electrodes)])
    
    aux=1/n_electrodes
    for elec in range(0,n_electrodes):
        signal_car[:,elec]=signal[:,elec]-aux*sig_ac
        
    return signal_car
    