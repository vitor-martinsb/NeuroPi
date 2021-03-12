import numpy as np
import math as mt

def pre_cca(Signal,freq,fs,t):
    
    n_freq=len(freq)
    T_collect=np.arange(0,t,1/fs)
    
    for f in range n_freq:
        Y_f=mt.sin()