import numpy as np
import classificador as cl

def selec_atrib(Xt,R,n_elec,n_freq):

    H=Xt[:,0:n_elec*n_freq]
    rho=np.zeros((n_elec,1))
    rho_matriz=np.zeros((n_freq,n_freq))
    matriz_ord=np.zeros((n_elec,2))
    L,C=np.shape(R)
    
    for elec in range(0,n_elec):
        ini=0+elec*4
        fim=4+elec*4
        H_aux=H[:,ini:fim]
        
        for a in range(0,C):  
            
            for b in range(0,C):
            
                x_mean=np.mean(H_aux[:,a])
                y_mean=np.mean(R[:,b])
                
                soma_cov=0
                x_aux=0
                y_aux=0
                
                
                for n in range(0,L):
                    soma_cov=((H_aux[n,a]-x_mean)*(R[n,b]-y_mean)) + soma_cov
                    x_aux=(H_aux[n,a]-x_mean)**2+x_aux
                    y_aux=(R[n,b]-y_mean)**2+y_aux
                
                soma_var=(x_aux*y_aux)**0.5             
                rho_matriz[a,b]=soma_cov/soma_var
        
        
        rho_matriz=abs(rho_matriz)
   
        for diag in range(0,n_freq):
            rho[elec]=rho[elec]+(rho_matriz[diag,diag])
    
    canais=np.argsort(-rho[:,0])
    c=np.sort(-rho[:,0])        
    
    matriz_ord[:,0]=canais
    matriz_ord[:,1]=-c
    return rho,matriz_ord

def define_melhor(Xt,Xv,R,n_elec,n_freq,matriz_ord,per_train,n_signal):
    
    MED_V=np.zeros([n_elec,1])
    MED_T=np.zeros([n_elec,1])
    STD_V=np.zeros([n_elec,1])
    STD_T=np.zeros([n_elec,1])
    Lv,Cv=np.shape(Xv)
    Lt,Ct=np.shape(Xt)
    canais=matriz_ord[:,0]
    ordem=matriz_ord[:,1]
    Xt_selec=np.zeros([Lt,n_freq+1])
    Xv_selec=np.zeros([Lv,n_freq+1])
    c=np.zeros([1,1])
    
    for elec in range(0,n_elec):
        del c
        c=np.zeros([1,elec])
        c=canais[0:elec+1]
        
        del Xt_selec
        del Xv_selec
        Xt_selec=np.zeros([Lt,((elec+1)*4) + 1])
        Xv_selec=np.zeros([Lv,((elec+1)*4) + 1])
        
        for e in range(0,elec+1):
            ini_Xt=int(0+c[e]*4)
            fim_Xt=int(4+c[e]*4)
            
            ini_Xt_selec=int(0+e*4)
            fim_Xt_selec=int(4+e*4)
           
            Xt_selec[:,ini_Xt_selec:fim_Xt_selec]=Xt[:,ini_Xt:fim_Xt]
            Xv_selec[:,ini_Xt_selec:fim_Xt_selec]=Xv[:,ini_Xt:fim_Xt]
        
        Xt_selec[:,((elec)*4) + 1]=Xt[:,Ct-1]
        Xv_selec[:,((elec)*4) + 1]=Xv[:,Cv-1]
        
        [w,R]=cl.return_w(Xt_selec,n_freq)
        Yt=cl.return_y(Xt_selec,w,n_freq,per_train,n_signal)
        Yv=cl.return_y(Xv_selec,w,n_freq,per_train,n_signal)
        
        RES_V,cont_V,MED_V[elec],STD_V[elec]=cl.result(Yv,n_freq)
        RES_T,cont_T,MED_T[elec],STD_T[elec]=cl.result(Yt,n_freq)
   
    #print(np.shape(MED_V),np.shape(STD_V),np.shape(MED_T),np.shape(STD_T))
    MED_V=np.transpose(MED_V)
    MED_T=np.transpose(MED_T)
    STD_V=np.transpose(STD_V)
    STD_T=np.transpose(STD_T)
    return MED_V,STD_V,MED_T,STD_T,canais,ordem
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        