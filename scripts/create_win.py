import numpy as np
import os

def win(FOLD,n_win,trial,freq,t_collect,fs,t_ini):
    os.chdir(FOLD)
    print(FOLD)
    for f in freq:
        for t in trial:
            fileName='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t)+'.npy'
            signal=np.load(fileName)
            sig=signal[t_ini*fs:t_collect*fs,:]
            aux=(fs*(t_collect-t_ini))/n_win
            aux=int(aux)
            cont=0
            
            for w in range(0,n_win):
                fileName_new='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t)+'_'+str(w)+'.npy'
                sig_W=sig[aux*cont:aux*(cont+1),:]
                cont=cont+1
                np.save(fileName_new,sig_W)
            