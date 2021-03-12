


import os
import scipy.io as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time as tm
from random import *

fs=250
t_collect_t=3
n_trial=8
freq=[6,10,12,15]
n_elec=8
n_win=4
individuo='Caio'

FOLD_ent='/home/pi/Desktop/BCI/Offline_system/OpenBCI/scripts/Data_record/'+individuo+'/Data_FILT'
FOLD_sai='/home/pi/Desktop/BCI/Offline_system/OpenBCI/scripts/Data_record/'+individuo+'/Data_MAT/'

for t in range(1,n_trial+1):
    for f in freq:
        for w in range(0,n_win):
            os.chdir(FOLD_ent)
            fileNameIN='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t)+'_'+str(w)+'.npy'
            fileName='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t)+'_'+str(w)+'.mat'
            signal=np.load(fileNameIN)
            os.chdir(FOLD_sai)
            sp.savemat(FOLD_sai+fileName, mdict={'signal': signal})