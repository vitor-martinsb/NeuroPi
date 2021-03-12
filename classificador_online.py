import numpy as np
import os
import scipy.io as sp
from scipy.fftpack import fft
import time as tm
import Fcar as fc

#Gera a base do classificador
def gera_base(n_trial,n_win,n_freq,n_elec,freq,fs,t_collect,t_ini,FOLD,teste): 

    X=np.zeros([n_trial*n_win*n_freq,n_elec*n_freq]);
    t_collect_T=int((t_collect-t_ini)/n_win) #Tempo de coleta
    os.chdir(FOLD)
    L_cont=0
    
    
    for f in freq: #para cada freq
        for t in range(0,n_trial): #para cada trial
            for w in range(0,n_win): #para cada janela
                
                    
                    if teste==1: # para dados do sistema adquirido G-TECH
                        filename='SSVEP_'+str(f)+'Hz_'+'Trial'\
                        +str(t+1)+'_'+'SUBJ10_'+str(w+1)+'.mat'
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
                    else: # para dados adquiridos via OpenBCI
                        
                        filename='SSVEP_'+str(f)+'Hz_'+'Trial'+\
                        str(t+1)+'_'+str(w)+'.npy';
                        signal=np.load(filename)
                       
                    L,C=np.shape(signal)
                    vet_aux=np.zeros([n_elec*n_freq]);
                        
                    cont=0
                
                    for e in range(0,n_elec): # Para cada eletrodo, fft calculada
                    
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
    return(X) #retorna X

def div_base(X,n_signal,per_train,dim_sig,n_freq): #divide a base para
                                                    #validação e treubi
   #auxiliares
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
        X_f=np.array(range(0,aux))+k*aux #Seleciona por sorteio os indices de X
        np.random.shuffle(X_f);
        
        X_v_pos[k,:]=X_f[0:aux_v] #Atribui uma matriz validação
        X_t_pos[k,:]=X_f[aux_v:aux_v+aux_t] #Atribuiuma matriz treinamento

    cont=0
    for k in range(0,n_freq):
        for k1 in range(0,aux_t):
            POS=int(X_t_pos[k,k1]); #Atribui os sinais para treino
            Xt[cont,:]=X[POS,:];
            cont=cont+1
            
    cont=0        
    for k in range(0,n_freq):
        for k1 in range(0,aux_v): #Atribui os sinais para validação
            POS=int(X_v_pos[k,k1]);
            Xv[cont,:]=X[POS,:];
            cont=cont+1

    return(Xv,Xt,X_v_pos,X_t_pos) #Retorna matriz validação e matriz treino

def return_w(X,n_freq): #Calcula os vetores de peso
    
    L,C=np.shape(X)
    
    R=np.ones([L,n_freq]) #matriz de rotulos
    n_S=L/n_freq
    
   
    for f in range(0,n_freq):
        for s in range(0,L):
            if s>=f*n_S and s<(f+1)*n_S:
                R[s,f]=R[s,f]
            else:
                R[s,f]=-R[s,f]
         
    Xinv=np.linalg.pinv(X) #Calcula a inversa de X
    w=np.zeros([n_freq,C])
    
    for k in range(0,n_freq):
        w[k,:]=np.dot(Xinv,R[:,k]); #Calcula os pesos

    return(w,R)

def return_y(Xv,w,n_freq): #Retorna a matriz de valores
    
    L=np.shape(Xv)
    y=np.zeros([L[0],n_freq])
    w=np.transpose(w)
    
    y=np.dot(Xv,w) #Calcula para cada aquisição
        
    return (y)

def result(Yv,n_freq): #Caclula os resultados
   
    fr=np.max(Yv)
    freq=[6,10,12,15]
    c=0
    
    for f in range(0,n_freq):
        aux=Yv[0,c]
        if aux==fr:
            fr=freq[c]
            return(fr)
        c=c+1