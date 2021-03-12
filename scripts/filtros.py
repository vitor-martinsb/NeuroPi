import numpy as np
import Fcar as fc
from scipy import signal

def aplica_filter(filter_order,f_low,f_high,fs,t,data,op):
    
    sig_F=np.zeros([fs*t,1])
    
    if  op==1:
        
        nyq = 0.5 * fs
        normal_cutoff = f_low / nyq
        b, a = signal.butter(filter_order, normal_cutoff, btype='low', analog=False)
        sig_F = signal.lfilter(b,a,data)
        return sig_F
    
    elif op==2:
        
         nyq = 0.5 * fs
         normal_cutoff = f_high / nyq
         b, a = signal.butter(filter_order, normal_cutoff, btype='high', analog=False)
         sig_F = signal.lfilter(b,a,data)
         return sig_F
        
    elif op==3:
        
         nyq = 0.5 * fs
         low = f_low / nyq
         high = f_high / nyq
         b, a = signal.butter(filter_order, [low, high], btype='band')
         sig_F=signal.lfilter(b,a,data)
         return sig_F
     
    elif op==4:
        Q=30.0
        w0 = f_low/(fs/2)
        b, a=signal.iirnotch(w0,Q);
        sig_F=signal.lfilter(b,a,data)
        
        return sig_F
    
def pre_proc(CAR,filters,filter_order,f_low,f_high,fs,t,signal,op,n_electrodes,t_collect):
    
    if CAR==1:
        sig=fc.car_filter(signal,n_electrodes,t_collect,fs)
    elif CAR==0:
        sig=signal
        
    if filters==1:
        for e in range (0,n_electrodes):
            sig[:,e]=aplica_filter(filter_order,5,50,fs,t_collect,signal[:,e],3)
            sig[:,e]=filt.aplica_filter(filter_order,60,[],fs,t_collect,sig[:,e],4)
            
    return sig