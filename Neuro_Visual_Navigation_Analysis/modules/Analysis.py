#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:10:39 2020

@author: tomasg
"""

#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO





import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pickle
from scipy.ndimage import gaussian_filter as gauss_fil
from os import listdir
from skimage import measure
from scipy.ndimage import rotate
from matplotlib.figure import Figure


def Mover_Imagen(image,x,y):
    Diaba=image
    if (x>=0):
        Da=np.zeros([35,35+x])
        Diaba=np.append(Diaba, Da,axis=1)
        Diaba=np.append(Da[:,:35-x], Diaba,axis=1)
    elif (x<0):
        Da=np.zeros([35,35-x])
        Diaba=np.append(Da, Diaba,axis=1)
        Diaba=np.append(Diaba,Da[:,:35+x] ,axis=1)
    if (y>=0):
        Da=np.zeros([35+y,105])
        Diaba=np.append(Diaba, Da,axis=0)
        Diaba=np.append(Da[:35-y,:], Diaba,axis=0)
    elif (y<0):
        Da=np.zeros([35-y,105])
        Diaba=np.append(Da, Diaba,axis=0)
        Diaba=np.append(Diaba, Da[:35+y,:],axis=0)
     #plt.imshow(Diaba,cmap="jet")        
    return Diaba

def Mapa_Corr(Image_org, min_spikes = 20):

    Mapa_c=np.zeros([70,70])

    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_org,i,j)[35:70,35:70]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))
                Mapa_c[35+i][35+j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35+i][35+j]=np.nan
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_org,-i,-j)[35:70,35:70]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))
                Mapa_c[35-i][35-j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35-i][35-j]=np.nan
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_org,-i,j)[35:70,35:70]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))            
                Mapa_c[35-i][35+j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35-i][35+j]=np.nan
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_org,i,-j)[35:70,35:70]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))                        
                Mapa_c[35+i][35-j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35+i][35-j]=np.nan

    Fig = Figure()
    ax1 = Fig.subplots()
    ax1.imshow(Mapa_c,cmap="jet")
    return Fig , Mapa_c


def Mapa_Cross_Corr(Image_Movil, Image_Fija):

    Mapa_c=np.zeros([70,70])
    
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_Movil,i,j)[35:70,35:70]
            Original=np.copy(Image_Fija)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>20:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))
                Mapa_c[35+i][35+j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35+i][35+j]=np.nan
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_Movil,-i,-j)[35:70,35:70]
            Original=np.copy(Image_Fija)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>20:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))
                Mapa_c[35-i][35-j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35-i][35-j]=np.nan
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_Movil,-i,j)[35:70,35:70]
            Original=np.copy(Image_Fija)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>20:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))            
                Mapa_c[35-i][35+j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35-i][35+j]=np.nan
    for i in range(35):
        for j in range(35):    
            Movida=Mover_Imagen(Image_Movil,i,-j)[35:70,35:70]
            Original=np.copy(Image_Fija)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>20:
                Diff=pd.DataFrame(np.concatenate((Original,Movida),axis=1))                        
                Mapa_c[35+i][35-j]=Diff.corr(method="pearson")[0][1]
            else:
                Mapa_c[35+i][35-j]=np.nan
    Fig = Figure()
    ax1 = Fig.subplots()
    ax1.imshow(Mapa_c,cmap="jet")
    return Fig , Mapa_c
        


def Propiedades_mapa_return_thres(map_correlacion):
    """Funcion para determinar las propiedas de las regiones del mapa de grilla. Retorna las 
    propiedades del mapa y el mapa umbrelizado"""
    map_correlacion[map_correlacion>0.2]=1
    map_correlacion[map_correlacion<=0.2]=0
    label=measure.label(map_correlacion)
    propiedades=measure.regionprops(label)
    return propiedades,map_correlacion

def Radio_inter_externo_distancia_segundo(propiedades,Corre):
    """Calculo de radio interno, externo y la distancia de los centros.
    radio interno: pixel más cercano al centro de la imagen (considerando los 6 cluster más cercanos)
    radio externo: centro más alejado del centro de la imagen (considerando los 6 cluster más cercanos)
    """
    center_x=Corre.shape[0]/2
    center_y=Corre.shape[1]/2
    distancia_x=[reg.centroid[0] for reg in propiedades]
    distancia_y=[reg.centroid[1] for reg in propiedades]
    distancias=Calculo_distancias(distancia_x, distancia_y,center_x,center_y)
    radio_interno=Calculo_radio_interno(propiedades,distancias, center_x, center_y)
    distancias_copy=distancias.copy()
    distancias_copy.sort()
    distancias_copy = distancias_copy[1:7]

   # radio_externo = Calculo_radio_externo(propiedades,distancias, center_x, center_y)
    radio_externo = distancias_copy[len(distancias_copy)-1]

    return distancias,radio_interno,radio_externo

def Recort_inferior(corr, radio_interno, center_x, center_y):
    """Elimina todos los valores que se encuentran dentro de una circunferencia
    delimitada por el radio interno (centrada en la imagen)"""
    matriz_verificacion=np.zeros_like(corr)
    matriz_verificacion[matriz_verificacion==0]=False
    for i in range(matriz_verificacion.shape[0]):
        for j in range(matriz_verificacion.shape[1]):
            if np.sqrt(np.square(i-center_x) + np.square(j-center_y) )<=radio_interno:
                matriz_verificacion[i][j]=True
    co=np.copy(corr)
    co[matriz_verificacion==True]=np.nan
    return co

def Recort_superior(corr, radio_externo, center_x, center_y):
    """Elimina todos los valores que se encuentran dentro de una circunferencia
    delimitada por el radio interno (centrada en la imagen)"""
    matriz_verificacion=np.zeros_like(corr)
    matriz_verificacion[matriz_verificacion==0]=False
    for i in range(matriz_verificacion.shape[0]):
        for j in range(matriz_verificacion.shape[1]):
            if np.sqrt(np.square(i-center_x) + np.square(j-center_y) )>=radio_externo:
                matriz_verificacion[i][j]=True
    co=np.copy(corr)
    co[matriz_verificacion==True]=np.nan
    return co

def Recortar_mapa(Corr, radio_interno, radio_externo, center_x, center_y):
    """Funcion que recorto la imagen dejando los valores entre el radio interno
    y el externo"""
    corr_to_recort= np.copy(Corr)
    corr_to_recort=Recort_inferior(corr_to_recort,radio_interno, center_x, center_y)
    corr_to_recort=Recort_superior(corr_to_recort,radio_externo, center_x, center_y)
    return corr_to_recort

def Eliminar_nan(mapa1, mapa2):
    """Elimina ordenadamete los nan de ambos mapas"""
    vect1=mapa1.flatten()
    vect2=mapa2.flatten()
    vect1[np.isnan(vect1)]=900
    vect2[np.isnan(vect2)]=900
    auxiliar_1=np.take(vect1,np.where(vect2!=900))
    auxiliar_2=np.take(vect2,np.where(vect1!=900))
    vect1=np.take(auxiliar_1,np.where(auxiliar_1[0]!=900))
    vect2=np.take(auxiliar_2,np.where(auxiliar_2[0]!=900))
    return vect1,vect2
    
def Eliminar_zeros(mapa1, mapa2):
    """Elimina ordenadamete los 0 de ambos mapas"""
    vect1=mapa1.flatten()
    vect2=mapa2.flatten()
    vect1[vect1==0]=900
    vect2[vect2==0]=900
    auxiliar_1=np.take(vect1,np.where(vect2!=900))
    auxiliar_2=np.take(vect2,np.where(vect1!=900))
    vect1=np.take(auxiliar_1,np.where(auxiliar_1[0]!=900))
    vect2=np.take(auxiliar_2,np.where(auxiliar_2[0]!=900))
    return vect1,vect2

def Propiedades_mapa_return_thres(map_correlacion):
    """Funcion para determinar las propiedas de las regiones del mapa de grilla. Retorna las 
    propiedades del mapa y el mapa umbrelizado"""
    map_correlacion[map_correlacion>0.2]=1
    map_correlacion[map_correlacion<=0.2]=0
    label=measure.label(map_correlacion)
    propiedades=measure.regionprops(label)
    return propiedades,map_correlacion

def Eliminar_zeros(array1, array2):
    array2 = np.nan_to_num(array2).flatten()
    array1 = np.nan_to_num(array1).flatten()
    array2_tmp = np.take(array2, np.where(array1 != 0))
    array1_tmp = np.take(array1, np.where(array2 != 0))
    array2 = np.take(array2_tmp, np.where(array2_tmp[0] != 0))
    array1 = np.take(array1_tmp, np.where(array1_tmp[0] != 0))
    return array1.T, array2.T

def Calculo_dist_radial(lista, center_x, center_y):
    """Devuelve una lista con las distancias de cada pixel al centro"""
    radio_interno=lista.coords-(center_x, center_y)
    radio_interno=np.square(radio_interno)
    radio_interno=np.sum(radio_interno,axis=1)
    radio_interno=np.sqrt(radio_interno)
    return radio_interno

def Calculo_radio_interno(propiedades, distancias, center_x, center_y):
    """Devuelve el radio interno (para eliminar el centroide del centro)"""

    distancias_copy=distancias.copy()
    distancias_copy.sort()
    distancias_copy=distancias_copy[1:7]
    dist_regions=[]
    for i in distancias_copy:
        region=distancias.index(i)        
        dist_regions.append(min(Calculo_dist_radial(propiedades[region], center_x, center_y) ) )
    radio_interno=min(dist_regions)
    return radio_interno        

def Selecion_distancia_maxima(distancia):
    """Selecciona el radio externo de tal forma de asegurarse
    de que el radio seleccionado no sea mayor a 30"""
    if int(distancia[len(distancia)-1])<30:
        return distancia[len(distancia)-1]
    else:
        return Selecion_distancia_maxima(distancia[:len(distancia)-1])

def Calculo_radio_externo(propiedades, distancias, center_x, center_y):
    """Devuelve el radio externo (para segmentar unicamente los 6 patrones
    centrale"""
    distancias_copy=distancias.copy()
    distancias_copy.sort()
    distancias_copy=distancias_copy[1:7]
    dist_regions=[]
    for i in distancias_copy:
        region=distancias.index(i)        
        dist_regions.append(max(Calculo_dist_radial(propiedades[region], center_x,  center_y) ) )
    radio_externo=max(dist_regions)
    return radio_externo        

def Calculo_distancias(distancia_x, distancia_y,center_x,center_y):
    """Determino la distancia de los distintos centroides al centro del 
    mapa de correlacion"""
    fun_distancia=lambda x,y: np.sqrt(np.square(x-center_x)+np.square(y-center_y))
    distancias=list(map(fun_distancia,distancia_x,distancia_y))
    return distancias

def Calculo_grid_not_origin_extern_radios_variables(corre, date="none", clu1="none", clu2="none"):
    """ prueba calculando la corre con la imagen thresholdiada y variando el radio externo 
    para determinar el maximo grid score"""
    fig = Figure()
    center_x = corre.shape[0]/2
    center_y = corre.shape[1]/2
    mapa_corre = np.copy(corre)
    propiedades, mapa_corre=Propiedades_mapa_return_thres(mapa_corre)
    dist,radio_interno,radio_externo=Radio_inter_externo_distancia_segundo(propiedades,corre)   
    score=[]
    print(dist, radio_interno, radio_externo)
    if len(propiedades)>7:
        for radio_externo1 in range(int(radio_interno)+1,int(radio_externo)+10,1):
      #  for radio_externo in range(int(radio_interno),int(radio_externo),1):
            coef=[]
            for angle in range(30,180,30):
                # rotado2=Rotar(corre,angle,center_x,center_y)
                mapa_corre1=np.nan_to_num(mapa_corre.copy())
                mapa_rotado1=rotate(mapa_corre1,angle,reshape=False)
                mapa_rotado1=np.round(mapa_rotado1)
                mapa_rotado1=Recortar_mapa(mapa_rotado1, radio_interno, radio_externo1, center_x, center_y)
                mapa_corre1=Recortar_mapa(mapa_corre1, radio_interno, radio_externo1, center_x, center_y)
                if angle == 30:
                    ax = fig.subplots()
                    ax.imshow(mapa_corre1)        
                mapa_corre1, mapa_rotado1=Eliminar_nan(mapa_corre1, mapa_rotado1)
                # mapa_corre1, mapa_rotado1=Eliminar_zeros(mapa_corre1,mapa_rotado1)
                coef.append(np.corrcoef( mapa_corre1,mapa_rotado1)[0][1])
            grid_score_4=min([ coef[i] for i in [1, 3] ] )-max([coef[i] for i in [0, 2, 4] ] )
            score.append(grid_score_4)
        try:
            return max(score), fig
        except:
            print("No se puedo ejecutar la siguiente combinacion date")
    else:
        return np.nan, fig



###########################################################################
#        Generadon mapas disparo
###########################################################################

def Cluster_type_light_(Diccionario,luz_oscuridad,type_fuente,num_clu, bins = 25.0001):
    Eje_Temporal = Eje_Temporal_Func(Diccionario)
    """Devuelve Figure para mostrar"""
    Disparos_clu=np.array([])
    fuente="{}{}".format(str(type_fuente),".{}")
    for i in range(30):
        if fuente.format(i) in Diccionario["Cluster Numero {}".format(str(num_clu))][luz_oscuridad]:
            Disparos_clu=np.concatenate((Disparos_clu,Diccionario["Cluster Numero {}".format(str(num_clu))][luz_oscuridad][fuente.format(i)]))    
    Shots_clu=Disparos(Disparos_clu, Eje_Temporal) #Determino los disparos
    Cuenta=Cuentas(Shots_clu,Diccionario["Posicion"].T[0], Diccionario["Posicion"].T[1], bins)
    Time=Tiempo_2(Diccionario, bins,type_fuente) #Tiempo del individuo en una determinada posicion
    Tasa_de_disparo=Tasa_disparo(Cuenta, Time)
    Imagen_Filtrada=gauss_fil(Tasa_de_disparo, 1)
    Fig = Figure()
    ax1 = Fig.subplots()
    ax1.imshow(Imagen_Filtrada,cmap="jet")
    return Fig , Imagen_Filtrada

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

def Cuentas(disp_clu,posx,posy,bins):
    """Funcion que determina el número total de disparos den un determinado lugar fisico. Se representa por medio de 
    una matriz"""
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(900/bins),int(900/bins)])
    for i in range(disp_clu.shape[0]):
        Tasa_disparo[int(Y[int(disp_clu[i])]/bins)][int(X[int(disp_clu[i])]/bins)]+=1
    return Tasa_disparo


def Tiempo_2(Dicc,bins,type_fuente):
    """Funcion que determina el tiempo total que el animal paso en un determinado lugar fisico en unos determinados 
    intervalos. Se representa por medio de una matriz"""
    Tasa_disparo=np.zeros([int(900/bins),int(900/bins)])
    for i in range(60):
        if Dicc["Light_Trials"][i][1]==type_fuente:
            X=list(Dicc["Posicion"].T[0][int(int(Dicc["Light_Trials"][i][2])/400):int(int(Dicc["Light_Trials"][i][3])/400)+1])
            Y=list(Dicc["Posicion"].T[1][int(int(Dicc["Light_Trials"][i][2])/400):int(int(Dicc["Light_Trials"][i][3])/400)+1])
            for i in range(len(X)):
                if (Y[i]!=-1 or X[i]!=-1):
                    Tasa_disparo[int(Y[i]/bins)][int(X[i]/bins)]+=400
    return Tasa_disparo/20000       #Se divide por 20k para obtener la matriz expresada en segundos

def Tasa_disparo(cuenta,tiempo):
    """Funcion que determina la tasa de disparo"""
    #La variable tiempo es el Eje_temporal
    tasa_verdadera=np.zeros(cuenta.shape)
    for i in range(cuenta.shape[0]):
        for j in range(cuenta.shape[0]):
            if tiempo[i][j]!=0:
                tasa_verdadera[i][j]=cuenta[i][j]/tiempo[i][j]
    return tasa_verdadera

def Eje_Temporal_Func(Diccionario):
    eje_temporal = np.zeros(Diccionario["Posicion"].T.shape[1])
    for i in range(eje_temporal.shape[0]):
        eje_temporal[i]=400*(i+1)
    return eje_temporal




def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic

#########################################################
# Main funcitions
#########################################################


if __name__ == "__main__":
    print("Se ejecutó modo manual")
  