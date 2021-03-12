import sys; sys.path.append('..') # help python find cyton.py relative to scripts folder
import numpy as np
import os
import matplotlib.pyplot as plt
import filtros as filt
import Fcar as fc

n_electrodes=16
t_collect=14

if n_electrodes==16:
    fs=125
else:
    fs=250
    
n_trial=8
freq=np.array([6,10,12,15])
filter_order=8
t_ini=2
sig_F=np.zeros([fs*t_collect,n_electrodes])
filter_car=1
individuo='Individuo'

if n_electrodes==16:
    fs=125
else:
    fs=250
    
for f in freq:
    for t in range (0,n_trial):
        for elec in range(0,n_electrodes):
            os.chdir('/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_ORI')
            fileName='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t+1)+'.npy'
            
            signal=np.load(fileName)
            if filter_car==1:
                signal=fc.car_filter(signal,n_electrodes,t_collect,fs)
            s_Data='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t+1);
          
            sig_F[:,elec]=filt.aplica_filter(filter_order,5,50,fs,t_collect,signal[:,elec],3)
            sig_F[:,elec]=filt.aplica_filter(filter_order,60,[],fs,t_collect,sig_F[:,elec],4)
        print(fileName)
        os.chdir('/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT')
        np.save(s_Data,sig_F)
        os.chdir('/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_ORI')
                #fig, axarr = plt.subplots(2,1)
                #axarr[0].plot(np.arange(0,t_collect-t_ini,1/fs),signal[fs*t_ini:t_collect*fs,elec])
                #axarr[0].set(title="Sinal sem filtro",xlabel="Tempo (s)", ylabel="Amplitude (V)")
                    
                #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.8, hspace=0.8)
                
                #axarr[1].plot(np.arange(0,t_collect-t_ini,1/fs),sig_F[fs*t_ini:t_collect*fs,elec])
                #axarr[1].set(title="Sinal filtro",xlabel="Tempo (s)", ylabel="Amplitude (V)")
                
                #fname='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t)+'_ele'+str(elec)+'_filt.png'
                #os.chdir('/home/pi/Desktop/BCI/Offline_system/OpenBCI/scripts/Data_record/Imagens')
                #plt.savefig(fname)
                #plt.show()
                
             