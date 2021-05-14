import numpy as np
from matplotlib import pyplot as plt
import pickle
import matplotlib as pl
from scipy.ndimage import gaussian_filter as gauss_fil

def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic

def Graficar_Disparo(disp_clu,posx,posy):
    """Funcion que grafica los puntos donde hubo disparo"""
    X=list(posx)
    Y=list(posy)
    for i in disp_clu:
        plt.plot(X[int(i)],Y[int(i)],"Dr")

def Disparos(clu,time):
    """Funcion que crea un vector donde cada elemento es un numero entero que representa el lugar donde estaba el SUJETO 
    cuando se registro el disparo. Esto es, los elementos del vector representan el INDICE 
    en el Eje_Temporal en el que sucedio el disparo."""
    posicion_disparo=np.array([])
    j=0
    for i in range(clu.shape[0]):
        Condicion=True
        while Condicion:
            if (clu[i]>=time[j] and clu[i]<time[j+1]):
                posicion_disparo=np.insert(posicion_disparo,posicion_disparo.shape[0],j)
                break
            j+=1
    return posicion_disparo


#####                                       Lectura de la posicion                                          #####
Posicion_X_Y=np.loadtxt('/home/tomasg/Escritorio/Neuro/Lectura de Datos/jp693-05062015-0108.whl')
#####Creo el vector que contiene el eje temporal de la posicion####
Eje_Temporal=np.zeros([Posicion_X_Y.shape[0]])
#####Lectura de los disparos (Clusers)####


def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic

def Graficar_Disparo(disp_clu,posx,posy):
    """Funcion que grafica los puntos donde hubo disparo"""
    X=list(posx)
    Y=list(posy)
    for i in disp_clu:
        plt.plot(X[int(i)],Y[int(i)],"Dr")

def Disparos(clu,time):
    """Funcion que crea un vector donde cada elemento es un numero entero que representa el lugar donde estaba el SUJETO 
    cuando se registro el disparo. Esto es, los elementos del vector representan el INDICE 
    en el Eje_Temporal en el que sucedio el disparo."""
    posicion_disparo=np.array([])
    j=0
    for i in range(clu.shape[0]):
        Condicion=True
        while Condicion:
            if (clu[i]>=time[j] and clu[i]<time[j+1]):
                posicion_disparo=np.insert(posicion_disparo,posicion_disparo.shape[0],j)
                break
            j+=1
    return posicion_disparo


#####                                       Lectura de la posicion                                          #####
Posicion_X_Y=np.loadtxt('/home/tomasg/Escritorio/Neuro/Lectura de Datos/jp693-05062015-0108.whl')
#####Creo el vector que contiene el eje temporal de la posicion####
Eje_Temporal=np.zeros([Posicion_X_Y.shape[0]])
#####Lectura de los disparos (Clusers)####


"""INICIALIZANDO VECTOR TEMPORAL"""

for i in range(Eje_Temporal.shape[0]):
    Eje_Temporal[i]=400*(i+1)
    
"""Reestructuro los datos posicion"""

Posicion_X_Y=Posicion_X_Y.reshape([2,427125])
pos_X=Posicion_X_Y[0]
pos_Y=Posicion_X_Y[1]
del Posicion_X_Y        #Elimino el vector para liberar espacio de memoria RAM
Dic=Cargar("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/jp693/Diccionario_0506")
Shots_clu=[]
Shots_clu=Disparos(Dic["Cluster Numero 3"]["Luz"]["l2.10"], Eje_Temporal)
Graficar_Disparo(Shots_clu, pos_X, pos_Y)



"""Funcion para el conteo"""

Tasa_disparo=np.zeros([167,167])
def Cuentas(disp_clu,posx,posy,bins):
    """Funcion que determina el número total de disparos den un determinado lugar fisico. Se representa por medio de 
    una matriz"""
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(835/bins+1),int(835/bins+1)])
    for i in range(disp_clu.shape[0]):
        Tasa_disparo[int(Y[int(disp_clu[i])]/bins)][int(X[int(disp_clu[i])]/bins)]+=1
    return Tasa_disparo

def Tiempo(posx,posy,bins):
    """Funcion que determina el tiempo total que el animal paso en un determinado lugar fisico. Se representa por medio
    de una matriz"""
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(835/bins+1),int(835/bins+1)])
    for i in range(posx.shape[0]):
        Tasa_disparo[int(Y[i]/bins)][int(X[i]/bins)]+=400
    return Tasa_disparo/20000       #Se divide por 20k para obtener la matriz expresada en segundos

def Tasa_disparo(cuenta,tiempo):
    """Funcion que determina la tasa de disparo"""
    tasa_verdadera=np.zeros(cuenta.shape)
    for i in range(cuenta.shape[0]):
        for j in range(cuenta.shape[0]):
            if tiempo[i][j]!=0:
                tasa_verdadera[i][j]=cuenta[i][j]/tiempo[i][j]
    return tasa_verdadera
                       
"""INICIALIZANDO VECTOR TEMPORAL"""

for i in range(Eje_Temporal.shape[0]):
    Eje_Temporal[i]=400*(i+1)
    
"""Reestructuro los datos posicion"""
def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic

def Graficar_Disparo(disp_clu,posx,posy):
    """Funcion que grafica los puntos donde hubo disparo"""
    X=list(posx)
    Y=list(posy)
    for i in disp_clu:
        plt.plot(X[int(i)],Y[int(i)],"Dr")

def Disparos(clu,time):
    """Funcion que crea un vector donde cada elemento es un numero entero que representa el lugar donde estaba el SUJETO 
    cuando se registro el disparo. Esto es, los elementos del vector representan el INDICE 
    en el Eje_Temporal en el que sucedio el disparo."""
    posicion_disparo=np.array([])
    j=0
    for i in range(clu.shape[0]):
        Condicion=True
        while Condicion:
            if (clu[i]>=time[j] and clu[i]<time[j+1]):
                posicion_disparo=np.insert(posicion_disparo,posicion_disparo.shape[0],j)
                break
            j+=1
    return posicion_disparo


#####                                       Lectura de la posicion                                          #####
Posicion_X_Y=np.loadtxt('/home/tomasg/Escritorio/Neuro/Lectura de Datos/jp693-05062015-0108.whl')
#####Creo el vector que contiene el eje temporal de la posicion####
Eje_Temporal=np.zeros([Posicion_X_Y.shape[0]])
#####Lectura de los disparos (Clusers)####


"""INICIALIZANDO VECTOR TEMPORAL"""

for i in range(Eje_Temporal.shape[0]):
    Eje_Temporal[i]=400*(i+1)
    
"""Reestructuro los datos posicion"""

Posicion_X_Y=Posicion_X_Y.reshape([2,427125])
pos_X=Posicion_X_Y[0]
pos_Y=Posicion_X_Y[1]
del Posicion_X_Y        #Elimino el vector para liberar espacio de memoria RAM
Dic=Cargar("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/jp693/Diccionario_0506")
Shots_clu=[]
Shots_clu=Disparos(Dic["Cluster Numero 3"]["Luz"]["l2.10"], Eje_Temporal)
Graficar_Disparo(Shots_clu, pos_X, pos_Y)



"""Funcion para el conteo"""

Tasa_disparo=np.zeros([167,167])
def Cuentas(disp_clu,posx,posy,bins):
    """Funcion que """
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(835/bins+1),int(835/bins+1)])
    for i in range(disp_clu.shape[0]):
        Tasa_disparo[int(Y[int(disp_clu[i])]/bins)][int(X[int(disp_clu[i])]/bins)]+=1
    return Tasa_disparo

def Tiempo(posx,posy,bins):
    """Funcion que """
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(835/bins+1),int(835/bins+1)])
    for i in range(posx.shape[0]):
        Tasa_disparo[int(Y[i]/bins)][int(X[i]/bins)]+=400
    return Tasa_disparo

def Calculo(cuenta,tiempo):
    tasa_verdadera=np.zeros(cuenta.shape)
    for i in range(cuenta.shape[0]):
        for j in range(cuenta.shape[0]):
            if tiempo[i][j]!=0:
                tasa_verdadera[i][j]=cuenta[i][j]/tiempo[i][j]
    return tasa_verdadera
                       

Posicion_X_Y=Posicion_X_Y.reshape([2,427125])
pos_X=Posicion_X_Y[0]
pos_Y=Posicion_X_Y[1]
del Posicion_X_Y        #Elimino el vector para liberar espacio de memoria RAM
Dic=Cargar("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/jp693/Diccionario_0506")
Shots_clu=[]
Shots_clu=Disparos(Dic["Cluster Numero 3"]["Luz"]["l2.10"], Eje_Temporal)
Graficar_Disparo(Shots_clu, pos_X, pos_Y)



"""Funcion para el conteo"""

Tasa_disparo=np.zeros([167,167])
def Cuentas(disp_clu,posx,posy,bins):
    """Funcion que """
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(835/bins+1),int(835/bins+1)])
    for i in range(disp_clu.shape[0]):
        Tasa_disparo[int(Y[int(disp_clu[i])]/bins)][int(X[int(disp_clu[i])]/bins)]+=1
    return Tasa_disparo

def Tiempo(posx,posy,bins):
    """Funcion que """
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(835/bins+1),int(835/bins+1)])
    for i in range(posx.shape[0]):
        Tasa_disparo[int(Y[i]/bins)][int(X[i]/bins)]+=400
    return Tasa_disparo

def Calculo(cuenta,tiempo):
    tasa_verdadera=np.zeros(cuenta.shape)
    for i in range(cuenta.shape[0]):
        for j in range(cuenta.shape[0]):
            if tiempo[i][j]!=0:
                tasa_verdadera[i][j]=cuenta[i][j]/tiempo[i][j]
    return tasa_verdadera
                       
verd=Calculo(Tasa, Frecuencia)
Frecuencia=Tiempo(pos_X, pos_Y, 15.001)/20000
Tasa=Cuentas(Shots_clu, pos_X, pos_Y,15.001)

plt.plot(Frecuencia)


Filtrado=gauss_fil(verd, 1)
plt.imshow(verd,cmap="jet",vmin=0,vmax=1)
plt.imshow(Filtrado,cmap="jet",vmin=0,vmax=1)
plt.imshow(Filtrado,cmap="YlOrBr_r",vmin=0,vmax=1)

p



