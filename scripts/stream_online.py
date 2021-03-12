import numpy as np
import os
import classificador_online as cl_online
import filtros as filt
import Fcar as fc
import time as tm
import sys; sys.path.append('..') 
from openbci import cyton as bci
import logging
from scipy import signal
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import selec_atrib as sa
import operator
import RPi.GPIO as GPIO
import _thread as td

#used for GPIO numbering
GPIO.setmode(GPIO.BCM) 
#closing the warnings when you are compiling the code
GPIO.setwarnings(False)
#defining the pins
LED1 = 20
LED2 = 21
LED3 = 22
LED4=  16
#defining the pins as output
GPIO.setup(LED1, GPIO.OUT) 
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

RUNNING = True

n_freq=4 #Número de frequências
n_trial=8 #aquisições feitas
freq=np.array([6,10,12,15]) # Frequências
n_elec=16 #Número de eletrodos

if n_elec==8:
    fs=250
else:
    fs=125
    
t_sinal=3 #Tempo de coleta
t_online=15
t_ini=2 #tempo inicial de aquisição
trial=[1,2,3,4,5,6,7,8] 
n_win=4 #Número de janelas
per_train=0.75 #Porcentagem de treinamento
individuo='Individuo' #Nome do individuo
create_win=0 
teste_class=0
n_signal=n_trial*n_win*n_freq #número de sinais
dim_sig=n_elec*n_freq  #número de sinais por eletrodo
cont_aq=-1
cont=-1
Data=np.zeros([fs*t_sinal,n_elec])
Data_f=np.zeros([fs*t_sinal*2,n_elec])
Data_f_all=np.zeros([fs*t_online,n_elec])
Data_aq=np.zeros([fs*t_online,n_elec])
Data_aq_OF=np.zeros([fs*t_sinal*2,n_elec])
Data_f_c_all=np.zeros([fs*t_online,n_elec])
seleciona_atributo=1

X=np.zeros([1,n_freq*n_elec+1])

cont_time=0

n_samples_aq=fs*t_online
n_samples=fs*t_sinal

#teste de valores
cont_freq=0
freq_teste=12

#Filtro passa banda 5 à 50 Hz
f_low=5
f_high=50
filter_order=8
nyq = 0.5 * fs
low = f_low / nyq
high = f_high / nyq
b_PB, a_PB = signal.butter(filter_order, [low, high], btype='band')

#Filtro notch 60 Hz
Q=30.0
w0 = 60/(fs/2)
b_FN, a_FN=signal.iirnotch(w0,Q);

# treino e filtro

treino=0
aplica_filtro=0
classifica_online=1
teste_aq_online=0
compara_cod=0

#Funções

def start_stream(board): #Inicia a gravacao
    global cont
    global cont_aq
    cont_aq=-1
    cont=-1 #inicia cont
    board.start_streaming(return_Data)
    board.stop
    board.print_bytes_in()
    
    
def return_Data(sample):
    
    global n_aq,n_freq
    global fs
    global t_sinal
    global cont
    global cont_aq
    global n_samples
    global Data
    global b_PB,a_PB
    global b_FN,a_FN
    global X,R,w
    global Data_f,Data_f_all
    global cont_time
    global cont_freq
    global freq_teste
    global seleciona_atributo
    global Data_f_c_all
    
    vet_aux=np.zeros([1,4])
    Data[cont,:]=sample.channel_data
    Data_aq[cont_aq,:]=Data[cont,:]
    cont=cont+1
    cont_aq=cont_aq+1
    L_cont=0

    xf=np.linspace(0,30,t_sinal*30)
    
    if cont==n_samples:
        if cont_aq==n_samples:
            Data_aq_OF[0:fs*t_sinal,:]=np.zeros([fs*t_sinal,n_elec])
            Data_aq_OF[fs*t_sinal:2*fs*t_sinal,:]=Data[:,:]
        else:
            Data_aq_OF[0:fs*t_sinal,:]=Data_aq[cont_aq-2*n_samples:cont_aq-n_samples,:]
            Data_aq_OF[fs*t_sinal:2*fs*t_sinal,:]=Data[:,:]
        
            
        
        for elec in range(0,n_elec):
            signal_f=signal.lfilter(b_PB,a_PB,Data_aq_OF[:,elec])
            signal_f=signal.lfilter(b_FN,a_FN,signal_f)
            Data_f[:,elec]=signal_f
        
        Data_f_c=fc.car_filter(Data_f,n_elec,2*t_sinal,fs)
        Data_f_c_all[cont_aq-n_samples:cont_aq,:]=Data_f_c[fs*t_sinal:2*fs*t_sinal]
        L_cont=0

        for e in range(0,n_elec): # Para cada eletrodo, fft calculada
                 
            sig=Data_f_c[:,e]
            sig_FFT=np.abs(fft(sig))/max(np.abs((fft(sig))))      
            
            for fr in freq:
                ind_fr=fr*(t_sinal)
                ind_fr=int(ind_fr)
                X[0,L_cont]=sig_FFT[ind_fr-1]
                L_cont=L_cont+1
       
        X[0,n_freq*n_elec]=1
        fr_result=-1
        if seleciona_atributo==1:
            
            C=np.shape(melhores_canais)
            C=int(4*C[0])
            Hv=np.ones([1,C+1])
            ini_H=0
            fim_H=4
            
            for elec in melhores_canais:
                ini=int(0+elec*4)
                fim=int(4+elec*4)
                Hv[:,ini_H:fim_H]=X[:,ini:fim]
                ini_H=ini_H+4
                fim_H=fim_H+4
            
            y=cl_online.return_y(Hv,w,n_freq)
        else:
            y=cl_online.return_y(X,w,n_freq)
            
        y=y[0,0:n_freq]
        fr_result=cl_online.result(y[0:n_freq])

        if fr_result==0:
            fr_result=6    
        elif fr_result==1:
            fr_result=10
        elif fr_result==2:
            fr_result=12
        elif fr_result==3:
            fr_result=15
            
        print('\n Frequência: '+str(fr_result)+'Hz \n')
        if freq_teste==fr_result:
            cont_freq=cont_freq+1
        cont=0
        Data=Data*0
        
        GPIO.output(LED1,GPIO.LOW)
        GPIO.output(LED2,GPIO.LOW)
        GPIO.output(LED3,GPIO.LOW)
        GPIO.output(LED4,GPIO.LOW)
        
        if fr_result==6:
            GPIO.output(LED1,GPIO.HIGH)
        elif fr_result==10:
            GPIO.output(LED2,GPIO.HIGH)
        elif fr_result==12:
            GPIO.output(LED3,GPIO.HIGH)       
        elif fr_result==15:
            GPIO.output(LED4,GPIO.HIGH)
        
        if cont_aq==n_samples_aq:
            print('\n Aquisição: '+str(cont_aq)+'\n')
            filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/Data_f_c_all.npy'
            np.save(filename,Data_f_c_all)
            filename='/home/pi/Desktop/BCI/online/scripts/Data_record/'+individuo+'/Data_FILT/Data_f_all.npy'
            np.save(filename,Data_f_all)
            os.chdir('/home/pi/Desktop/BCI/online/scripts/')
            tm.sleep(1)
            GPIO.output(LED1,GPIO.LOW)
            GPIO.output(LED2,GPIO.LOW)
            GPIO.output(LED3,GPIO.LOW)
            GPIO.output(LED4,GPIO.LOW)
            sys.exit()

def stream_data():
    n_freq=4 #Número de frequências
    n_trial=1 #Número de trials
    freq=np.array([6,10,12,15]) #frequências
    n_electrodes=16 #Número de eletrodos
    t_collect=3 #tempo de coleta (12 segundos) e 2 segundos para descarte
    if n_electrodes==16:
        fs=125
    else:
        fs=250
    n_samples=fs*t_collect #Número de amostras
    Data=np.zeros([n_samples,n_electrodes]) #Matriz de dados
    #auxiliares:
    freq_select=0 
    trial_select=0
    cont=0
    filtro_car=1
    filtro=1
    start_arm=1
    time_trash=3
    
    individuo='Individuo' #Nome do individuo
     
    if __name__ == '__main__':
        # port = '/dev/tty.OpenBCI-DN008VTF'
        #port = '/dev/tty.usbserial-DB00JAM0'
        # port = '/dev/tty.OpenBCI-DN0096XA'
        port = '/dev/ttyUSB0' #port
        baud = 115200 #bits
        logging.basicConfig(filename="test.log"\
        ,format='%(asctime)s - %(levelname)s : %(message)s',level=logging.DEBUG)
        logging.info('---------LOG START-------------')
        if n_elec==16:
            board = bci.OpenBCICyton(port=port, scaled_output=False, log=True, daisy=True)
            fs=125
        else:
            board = bci.OpenBCICyton(port=port, scaled_output=False, log=True)
            fs=250
            
        print("Board Instantiated")
        board.ser.write(str.encode('allon'))
        tm.sleep(3)
        #Cria e acessa pastas
    
        print("\n Press ENTER to start \n");
        OP=input()
        matriz_Data=start_stream(board)
        
        return matriz_Data
    
#Principal


if treino==1:
    runfile('/home/pi/Desktop/BCI/online/scripts/stream_time.py',\
    wdir='/home/pi/Desktop/BCI/online/scripts')
    
if aplica_filtro==1:
    runfile('/home/pi/Desktop/BCI/online/scripts/aplica_filtro.py',\
    wdir='/home/pi/Desktop/BCI/online/scripts/')
    runfile('/home/pi/Desktop/BCI/online/scripts/main.py',\
    wdir='/home/pi/Desktop/BCI/online/scripts')

if classifica_online==1:
    R=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/R.npy')
    w=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/w.npy')
    melhores_canais=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/canais.npy')    
    stream_data()
    
if teste_aq_online==1:
    R=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/R.npy')
    w=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/w.npy')
    sinal6=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_6Hz.npy')
    sinal10=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_10Hz.npy')
    sinal12=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_12Hz.npy')
    sinal15=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_15Hz.npy')
    
    sinal=fc.car_filter(sinal15,n_elec,t_online,fs)
    amostra_freq=t_sinal*18
    amostra_temp=t_sinal*fs
    ini=750;
    fim=ini+750;
    aux=int(t_online/t_sinal)
    
    mat_sig=np.zeros([fs*t_sinal,n_elec])
   
    for e in range(0,aux-1):
        fig, axs=plt.subplots(2)
        xt=np.linspace(0,t_sinal,amostra_temp)
        xf=np.linspace(0,18,amostra_freq)
            
        sig=sinal[ini:fim,1]
        
        sig_FFT=np.abs(fft(sig))/max(np.abs((fft(sig))))
        
        axs[0].plot(xt,sig)
        axs[0].set(xlabel='Tempo (s)', ylabel='Amplitude')
        axs[0].set_title('Sinal '+str(e))
        axs[1].plot(xf,sig_FFT[0:amostra_freq],'r')
        axs[1].set(xlabel='Frequência (Hz)', ylabel='Magnitude')
        plt.show()
        del fig,axs
        ini=ini+750
        fim=fim+750
    
    ini=750
    fim=ini+750
    
    for k in range(0,4):
        mat_sig=sinal[ini:fim,:]
        os.chdir('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
        +individuo+'/Data_FILT')
        filename='SSVEP_15Hz_Trial9_'+str(k)+'.npy'
        np.save(filename,mat_sig)
        
        ini=ini+750
        fim=fim+750
        
if compara_cod==1:
    
    Xv=np.ones([4,n_trial*n_win+1])
    R=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/R.npy')
    w=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
    +individuo+'/Data_FILT/w.npy')
    for k in range(0,4):
        Data_f_c=np.load('/home/pi/Desktop/BCI/online/scripts/Data_record/'\
        +individuo+'/Data_FILT/SSVEP_15Hz_Trial9_'+str(k)+'.npy')
        L_cont=0
        for e in range(0,n_elec): # Para cada eletrodo, fft calculada
                 
            sig=Data_f_c[:,e]
            sig_FFT=np.abs(fft(sig))/max(np.abs((fft(sig))))      
            
            for fr in freq:
                ind_fr=fr*(t_sinal)
                ind_fr=int(ind_fr)
                Xv[k,L_cont]=sig_FFT[ind_fr-1]
                L_cont=L_cont+1
            
    y=np.dot(Xv,np.transpose(w))