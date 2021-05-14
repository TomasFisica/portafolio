#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:46:22 2020

@author: tomasg
"""
#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO



import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.ndimage import gaussian_filter as gauss_fil
from os import listdir
import pandas as pd
# =============================================================================
# Los modulos cargados realizaran todo el trabajo fuerte.
# Aquí unicamente se organizara el trabajo
# =============================================================================
# Primero creo un data frame para ordenar

def Return_keys(dic, num_clu):
    """
    """
    Luz = dic["Cluster Numero {}".format(num_clu)]["Luz"].keys()
    Oscuridad = dic["Cluster Numero {}".format(num_clu)]["Oscuridad"].keys()
    return list(Luz), list(Oscuridad)

def Return_time_spike_sort(num_clu, dic):
    """Return a DataFrame with three columns Time Light  Cluster
    The DF is increasingly organized by the column time.
    The column time have the time where a cluster shot"""
    time = []
    light = []
    cluster = []
    keys_luz, keys_oscuridad = Return_keys(dic, num_clu)
    for luz in ["Luz", "Oscuridad"]:
        if luz == "Luz":
            keys=keys_luz
        else:
            keys=keys_oscuridad
        for key in keys:
            serie_times=dic["Cluster Numero {}".format(num_clu)][luz][key]
            list(map( time.append, serie_times ))
            list(map( light.append, [key[:2]]*len(serie_times)))
            list(map( cluster.append, [num_clu]*len(serie_times)))
    dic_prov = {"Time":time, "Light":light, "Cluster":cluster}        
    df1 = pd.DataFrame(dic_prov)
    df1.sort_values("Time", inplace = True)
    df1.set_index(pd.Index(range(len(df1))), inplace=True)
    return df1


def Time_axis(dic):
    Eje_Temporal=np.zeros(dic["Posicion"].T.shape[1])
    for i in range(Eje_Temporal.shape[0]):
        Eje_Temporal[i]=400*(i+1)
    return Eje_Temporal

def Map_Time(position, windows, bins = 25.0001):
    """Return the heat map about the time that the animal keep in some bins"""
    Tasa_disparo = np.zeros([int(900/bins),int(900/bins)])
    real_position = Cutout_position(position, windows)
    for x, y in real_position:
        if (y!=-1 or x!=-1):
            Tasa_disparo[int(y/bins)][int(x/bins)]+=400
    return Tasa_disparo/20000       #Se divide por 20k para obtener la matriz expresada en segundos

    
def Vector_shouts(spike):
    """Return a vector where eache value represent a index in matrix of position animal"""
    nex = lambda arg: round(arg/400)-1
    vector = list( map(nex, spike))
    return vector

def Map_shouts(vector_shouts, position, bins = 25.0001):
    """"""
    Tasa_disparo = np.zeros([int(900/bins),int(900/bins)])
    for index in vector_shouts:
        pos = position[index]
        if (pos[0]!=-1 or pos[1]!=-1):
            Tasa_disparo[int(pos[1]/bins)][int(pos[0]/bins)]+=1
    return Tasa_disparo

def Rate(map_shouts, map_time):
    
    division = map_shouts/map_time
    mapa = np.where(map_time != 0, division, 0)
    return mapa
    
    
def Map_Rate(spike, position, windows):
    """This funcion return a rate-spike mape"""
    map_time = Map_Time(position, windows)
    vector_shouts = Vector_shouts(spike)
    map_shouts = Map_shouts(vector_shouts, position)
    
    return map_time, map_shouts

def Cutout_spike(time_spike_sort, windows):
    """"""    
    time = time_spike_sort["Time"]
    time = time[(time>=windows[0]) & (time<=windows[1])]
    return time

def Cutout_position(position, windows):
    min_pos = int(windows[0]/400)-1
    max_pos = int(windows[1]/400)
    pos = position[min_pos : max_pos]
    return pos  
 
def Create_windows(dic):
    low_time = int(dic["Light_Trials"][0][2])
    high_time = int(dic["Light_Trials"][59][3])
    scale = high_time - low_time
    return low_time, high_time, scale

def Main(dic, num_clu, size_windows = 120, overlap = 2):

    time_spike_sort = Return_time_spike_sort(num_clu, dic)
    time_axis = Time_axis(dic)
    low_time, high_time, scale = Create_windows(dic)    
    num_windows = int(scale/(size_windows*20000) )
    high_time = low_time + size_windows*20000
    for i in range(num_windows):
        windows = [low_time, high_time]
        spike = Cutout_spike(time_spike_sort, windows)
        map_time, map_shouts = Map_Rate(spike, dic["Posicion"], windows)
        low_time += overlap*20000
        high_time += overlap*20000
        img = plt.imshow(mapa_rate)
        # plt.savefig("/home/tomasg/Escritorio/a{}".format(i))        
        yield map_time, map_shouts
        
a=Main(Dicc_clu, 5, 120, 120)
time=[]
shut=[]
Dicc_clu = Cargar("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/jp21414/Diccionario_3011")
for i in range(60):
    tim, shu= next(a)
    time.append(tim)
    shut.append(shu)
f=np.zeros_like(time[0])
g=np.zeros_like(time[0])
for ja in range(60):
    if Dicc_clu["Light_Trials"][ja][1]=="l3":
        f+=time[ja]
        g+=shut[ja]
divi=g/f
mapa_rate=np.where(f!=0,divi,0)
Imagen_Filtrada=gauss_fil(mapa_rate, 3)
plt.imshow(Imagen_Filtrada,cmap="jet")