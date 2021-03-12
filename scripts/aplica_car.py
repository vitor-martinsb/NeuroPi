import sys; sys.path.append('..') # help python find cyton.py relative to scripts folder
import numpy as np
import os
import matplotlib.pyplot as plt
import Fcar as fc

n_electrodes=3
t_collect=30
fs=250
n_trial=1
freq=np.array([6,10,12,15])

for f in freq:
        for t in range (1,n_trial+1):
            os.chdir('/home/pi/Desktop/BCI/Offline_system/OpenBCI/scripts/Data_record/Data_ORI')
            fileName='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t)+'.npy'
            signal=np.load(fileName)
            s_Data_CAR='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t+1)+'_CAR';
            sig_car=fc.car_filter(signal,n_electrodes,t_collect,fs)
            os.chdir('/home/pi/Desktop/BCI/Offline_system/OpenBCI/scripts/Data_record/Data_CAR')
            np.save(s_Data_CAR,sig_car)