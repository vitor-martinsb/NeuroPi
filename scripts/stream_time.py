import sys; sys.path.append('..') # help python find cyton.py relative to scripts folder
from openbci import cyton as bci
import logging
import time
import numpy as np
import os

n_freq=4
n_trial=8
freq=np.array([6,10,12,15])
n_electrodes=16
n_elec=16
t_collect=14

n_samples=fs*t_collect
Data=np.zeros([n_samples,n_electrodes])
freq_select=0
trial_select=0
cont=0
filtro_car=1
filtro=1
start_arm=1
time_trash=3
filter_order=8

if (n_elec==16):
    fs=125
else:
    fs=250


def start_stream():
    global cont
    cont=0
    board.start_streaming(return_Data)
    board.stop
    board.print_bytes_in()
    
def return_Data(sample):
    
    global trial_select
    global freq_select
    global freq
    global Data
    global n_samples
    global n_electrodes
    global cont
    global n_trial
    global n_freq
    global start_arm
    
    F=freq[freq_select]
    T=trial_select
    s_Data='SSVEP_'+str(F)+'Hz_'+'Trial'+str(T+1);
    
    Data[cont,:]=sample.channel_data
    cont=cont+1
    
    if cont==time_trash*fs and start_arm==1:
        cont=0
        start_arm=0
    
    
    if cont==n_samples and trial_select==n_trial-1 and freq_select==n_freq-1:
        print('\n Frequência: ' + str(F) + ' Trial: ' + str(T+1) + '\n Successfully transmitted ! \n Press ENTER to continue')
        OP=input()
        os.chdir('/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_ORI')
        np.save(s_Data,Data)
        os.chdir('/home/pi/Desktop/BCI/online/scripts')
    
        sys.exit()
  
    
    if cont==n_samples:
        print('\n Frequência: ' + str(F) + ' Trial: ' + str(T+1) + '\n Successfully transmitted ! \n Press ENTER to continue')
        OP=input()
        os.chdir('/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_ORI')
        np.save(s_Data,Data)
        os.chdir('/home/pi/Desktop/BCI/online/scripts')
        Data=np.zeros([n_samples,n_electrodes])
        start_arm=1
        cont=0

        if freq_select != n_freq-1:
            freq_select=freq_select+1
        else:
            freq_select=0
            if trial_select != n_trial-1:
                trial_select=trial_select+1
            else:
                trial_select=0
            
            
if __name__ == '__main__':
    # port = '/dev/tty.OpenBCI-DN008VTF'
    #port = '/dev/tty.usbserial-DB00JAM0'
    # port = '/dev/tty.OpenBCI-DN0096XA'
    port = '/dev/ttyUSB0'
    baud = 115200
    logging.basicConfig(filename="test.log",format='%(asctime)s - %(levelname)s : %(message)s',level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    if (n_elec==16):
        board = bci.OpenBCICyton(port=port, scaled_output=False, log=True, daisy=True)
        fs=125
    else:
        board = bci.OpenBCICyton(port=port, scaled_output=False, log=True)
        fs=250
        
    print("Board Instantiated")
    board.ser.write(str.encode('allon'))
    time.sleep(3)
    path_ind='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo
    os.mkdir(path_ind)
    os.mkdir(path_ind+'/Data_FILT');
    os.mkdir(path_ind+'/Data_CAR');
    os.mkdir(path_ind+'/Data_ORI');
    print("\n Press ENTER to start \n");
    OP=input()
    start_stream()
            
            
    
