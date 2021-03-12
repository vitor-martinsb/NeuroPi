import numpy as np
import os
import create_win as cw
import classificador as cl
import selec_atrib as sa

n_freq=4
n_trial=8
freq=np.array([6,10,12,15])
n_elec=16
t_collect=14
t_ini=2
trial=[1,2,3,4,5,6,7,8]
n_win=4
per_train=0.75
individuo='Individuo'
create_win=1
teste_class=0
n_signal=n_trial*n_win*n_freq
dim_sig=n_elec*n_freq
seleciona_atributo=1
itera=20

if n_elec==16:
    fs=125
else:
    fs=250
    

if create_win==1:
    FOLD='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT'
    cw.win(FOLD,n_win,trial,freq,t_collect,fs,t_ini)
    
    FOLD='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_ORI'
    cw.win(FOLD,n_win,trial,freq,t_collect,fs,t_ini)


FOLD='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT'

if teste_class==1:
    FOLD='C:/Users/Vitor/Desktop/Vitor/UFOP/IC-Parte-I/Dados/Nova_Base_3'
    
X=cl.gera_base(n_trial,n_win,n_freq,n_elec,freq,fs,t_collect,t_ini,FOLD,teste_class)


RES_V=np.zeros([itera,n_freq])
RES_T=np.zeros([itera,n_freq])
MED_V=np.zeros([itera,1])
MED_T=np.zeros([itera,1])
STD_V=np.zeros([itera,1])
STD_T=np.zeros([itera,1])
cont_V=np.zeros([itera,n_freq])
cont_T=np.zeros([itera,n_freq])

if seleciona_atributo==1:
    MED_V_MAT=np.zeros([itera,n_elec])
    MED_T_MAT=np.zeros([itera,n_elec])
    STD_V_MAT=np.zeros([itera,n_elec])
    STD_T_MAT=np.zeros([itera,n_elec])
    canais=np.zeros([itera,n_elec])
    ordem=np.zeros([itera,n_elec])
    ind_max_V=np.zeros([itera,1])
    ind_max_T=np.zeros([itera,1])
    
for k in range(0,itera):
    print('Iteração: ',k)
    if seleciona_atributo==0:
        Xv,Xt,Xv_pos,Xt_pos=cl.div_base(X,n_signal,per_train,dim_sig,n_freq)        
        [w,R]=cl.return_w(Xt,n_freq)
        Yv=cl.return_y(Xv,w,n_freq,per_train,n_signal)
        [w,R]=cl.return_w(Xt,n_freq)
        Yt=cl.return_y(Xt,w,n_freq,per_train,n_signal)
    
        RES_V[k,:],cont_V[k],MED_V[k],STD_V[k]=cl.result(Yv,n_freq)
        RES_T[k,:],cont_T[k],MED_T[k],STD_T[k]=cl.result(Yt,n_freq)
    else:
        Xv,Xt,Xv_pos,Xt_pos=cl.div_base(X,n_signal,per_train,dim_sig,n_freq)
        w,R=cl.return_w(Xt,n_freq)
        rho,matriz_ord=sa.selec_atrib(Xt,R,n_elec,n_freq)
        
        MED_V_MAT[[k],:],STD_V_MAT[[k],:],MED_T_MAT[[k],:],STD_T_MAT[[k],:],canais[[k],:],ordem[[k],:]=sa.define_melhor(Xt,Xv,R,n_elec,n_freq,matriz_ord,per_train,n_signal)
        
        if k==itera-1:
            for k in range(0,itera):
                ind_max_T[k]=np.argmax(MED_T_MAT[[k],:])
                ind_max_V[k]=np.argmax(MED_V_MAT[[k],:])
                MED_T[k]=np.max(MED_T_MAT[[k],:])
                MED_V[k]=np.max(MED_V_MAT[[k],:])
                STD_T[k]=np.min(STD_T_MAT[[k],:])
                STD_V[k]=np.min(STD_V_MAT[[k],:])

if seleciona_atributo==0:
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/R.npy'
    np.save(filename,R)
    
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/X.npy'
    np.save(filename,X)
    
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/w.npy'
    np.save(filename,w)
        
    print('\n Resultado treinamento:')
    print('\n Média de acertos:',np.sum(MED_T/itera),'%')
    
    
    print('\n Resultado validação:')
    print('\n Média de acertos:',np.sum(MED_V/itera),'%')
    
elif seleciona_atributo==1:
    
    print('\n Resultado treinamento:')
    ind_T=np.argmax(MED_T)
    L=int(ind_T)
    C=int(ind_max_T[L])+1
    print('Media de acertos:',np.max(MED_T),'%')
    print('Canais utilizados:',canais[L,0:C])
    
    print('\n Resultado validação:')
    ind_V=np.argmax(MED_V)
    L=int(ind_V)
    C=int(ind_max_V[L])+1
    print('Média de acertos',np.max(MED_V),'%')
    print('Canais utilizados:',canais[L,0:C])
    
    melhores_canais=canais[L,0:C]
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/canais.npy'
    np.save(filename,melhores_canais)
    
    Xv,Xt,Xv_pos,Xt_pos=cl.div_base(X,n_signal,per_train,dim_sig,n_freq)   
    C=np.shape(melhores_canais)
    C=int(4*C[0])
    H=np.ones([int(n_signal*per_train),C + 1])
    Hv=np.ones([n_signal-int(n_signal*per_train),C+1])
    ini_H=0
    fim_H=4
    
    for elec in melhores_canais:
        ini=int(0+elec*4)
        fim=int(4+elec*4)
        H[:,ini_H:fim_H]=Xt[:,ini:fim]
        Hv[:,ini_H:fim_H]=Xv[:,ini:fim]
        ini_H=ini_H+4
        fim_H=fim_H+4
        
  
    [w,R]=cl.return_w(H,n_freq)
    
    
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/R.npy'
    np.save(filename,R)
    
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/H.npy'
    np.save(filename,H)
    
    filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/w.npy'
    np.save(filename,w)
        
    Yv=cl.return_y(Hv,w,n_freq,per_train,n_signal)
    
    