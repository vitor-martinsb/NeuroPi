import numpy as np
import os
import scipy.io as sp
from scipy.fftpack import fft
import time as tm
import Fcar as fc
import operator

def gera_base(n_trial,n_win,n_freq,n_elec,freq,fs,t_collect,t_ini,FOLD,teste):

    X=np.zeros([n_trial*n_win*n_freq,n_elec*n_freq]);
    t_collect_T=int((t_collect-t_ini)/n_win)
    os.chdir(FOLD)
    L_cont=0
    for f in freq:
        for t in range(0,n_trial):
            for w in range(0,n_win):
                
                    
                    if teste==1:
                        filename='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t+1)+'_'+'SUBJ10_'+str(w+1)+'.mat'
                        mat=sp.loadmat(filename)
                        k=w+1
                        if k==1:
                            s = np.array(mat['v1'])
                        elif k==2:
                            s = np.array(mat['v2'])
                        elif k==3:
                            s = np.array(mat['v3'])
                        elif k==4:
                            s = np.array(mat['v4'])
                
                        signal=np.transpose(s);
                        signal=fc.car_filter(signal,n_elec,3,fs)
                    else:
                        
                        filename='SSVEP_'+str(f)+'Hz_'+'Trial'+str(t+1)+'_'+str(w)+'.npy';
                        signal=np.load(filename)
                       
                    L,C=np.shape(signal)
                    vet_aux=np.zeros([n_elec*n_freq]);
                        
                    cont=0
                
                    for e in range(0,n_elec):
                    
                        sig=signal[:,e]
                        sig_FFT=np.abs(fft(sig))/max(np.abs((fft(sig))))
                       
                        for fr in freq:
                            ind_fr=fr*(t_collect_T)
                            ind_fr=int(ind_fr)
                            vet_aux[cont]=sig_FFT[ind_fr]
                            cont=cont+1
                           
                    X[L_cont,:]=vet_aux[:]
                    L_cont=L_cont+1

    X=np.concatenate((X,np.ones([n_win*n_trial*n_freq,1])),axis=1);
    return(X)

def div_base(X,n_signal,per_train,dim_sig,n_freq):
    
    per_xt=int(n_signal*per_train)
    per_xv=int(n_signal*(1-per_train))
    aux_v=int(per_xv/n_freq)
    aux_t=int(per_xt/n_freq)

    Xt=np.zeros([per_xt,dim_sig+1]);
    Xv=np.zeros([per_xv,dim_sig+1]);
    aux=int(n_signal/n_freq)
    X_f=np.zeros([n_freq,aux])
    
    X_t_pos=np.zeros([n_freq,aux_t])
    X_v_pos=np.zeros([n_freq,aux_v])
    
    for k in range(0,n_freq):
        X_f=np.array(range(0,aux))+k*aux
        np.random.shuffle(X_f);
        
        X_v_pos[k,:]=X_f[0:aux_v]
        X_t_pos[k,:]=X_f[aux_v:aux_v+aux_t]

    cont=0
    for k in range(0,n_freq):
        for k1 in range(0,aux_t):
            POS=int(X_t_pos[k,k1]);
            Xt[cont,:]=X[POS,:];
            cont=cont+1
            
    cont=0        
    for k in range(0,n_freq):
        for k1 in range(0,aux_v):
            POS=int(X_v_pos[k,k1]);
            Xv[cont,:]=X[POS,:];
            cont=cont+1

    return(Xv,Xt,X_v_pos,X_t_pos)

def return_w(X,n_freq):
    
    L,C=np.shape(X)
    R=np.ones([L,n_freq])
    n_S=L/n_freq
    
   
    for f in range(0,n_freq):
        for s in range(0,L):
            if s>=f*n_S and s<(f+1)*n_S:
                R[s,f]=R[s,f]
            else:
                R[s,f]=-R[s,f]
         
    Xinv=np.linalg.pinv(X)
    w=np.zeros([n_freq,C])
    
    for k in range(0,n_freq):
        w[k,:]=np.dot(Xinv,R[:,k]);

    return(w,R)

def return_y(Xv,w,n_freq):
    
    L,C=np.shape(Xv)
    y=np.zeros([L,n_freq])
    w=np.transpose(w)
    for f in range(0,n_freq):
        y[:,f]=np.dot(Xv,w[:,f])
    return (y)

def result(Y): 
   
    max_index, max_value = max(enumerate(Y), key=operator.itemgetter(1))

        
    return (max_index)

