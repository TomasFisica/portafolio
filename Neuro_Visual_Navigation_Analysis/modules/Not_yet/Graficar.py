#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 13:36:15 2020

@author: tomas_vill
"""
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from scipy.ndimage import gaussian_filter as gauss_fil 


    
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
    return vect1[0],vect2[0]

def Mover_Imagen(image,x,y):
    Diaba=image
    if (x>=0):
        Da=np.zeros([70,70+x])
        Diaba=np.append(Diaba, Da,axis=1)
        Diaba=np.append(Da[:,:70-x], Diaba,axis=1)
    elif (x<0):
        Da=np.zeros([70,70-x])
        Diaba=np.append(Da, Diaba,axis=1)
        Diaba=np.append(Diaba,Da[:,:70+x] ,axis=1)
    if (y>=0):
        Da=np.zeros([70+y,210])
        Diaba=np.append(Diaba, Da,axis=0)
        Diaba=np.append(Da[:70-y,:], Diaba,axis=0)
    elif (y<0):
        Da=np.zeros([70-y,210])
        Diaba=np.append(Da, Diaba,axis=0)
        Diaba=np.append(Diaba, Da[:70+y,:],axis=0)
    #plt.imshow(Diaba,cmap="jet")        
        
    return Diaba

def Mapa_Corr(Image_org, min_spikes = 10):

    Mapa_c=np.zeros([140,140])

    for i in range(70):
        for j in range(70):    
            Movida=Mover_Imagen(Image_org,i,j)[70:140,70:140]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Mapa_c[70+i][70+j]=np.corrcoef(Movida, Original)[0][1]
            else:
                Mapa_c[70+i][70+j]=np.nan
    for i in range(70):
        for j in range(70):    
            Movida=Mover_Imagen(Image_org,-i,-j)[70:140,70:140]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Mapa_c[70-i][70-j]=np.corrcoef(Movida, Original)[0][1]
            else:
                Mapa_c[70-i][70-j]=np.nan
    for i in range(70):
        for j in range(70):    
            Movida=Mover_Imagen(Image_org,-i,j)[70:140,70:140]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Mapa_c[70-i][70+j]=np.corrcoef(Movida, Original)[0][1]
            else:
                Mapa_c[70-i][70+j]=np.nan
    for i in range(70):
        for j in range(70):    
            Movida=Mover_Imagen(Image_org,i,-j)[70:140,70:140]
            Original=np.copy(Image_org)
            Movida, Original= Eliminar_zeros(Movida, Original)
            if len(Movida)>min_spikes:
                Mapa_c[70+i][70-j]=np.corrcoef(Movida, Original)[0][1]
            else:
                Mapa_c[70+i][70-j]=np.nan
    return Mapa_c
















def Aux_Generator_fire_maps(dis):
    dis = d[1:]
    dis = dis[:-1]
    dis = np.array(Generator_list_fire(dis))
    plt.plot(dis.T[0], dis.T[1], "r*")


def Cuentas(disp_clu,posx,posy,bins = 25.000001):
    """Funcion que determina el número total de disparos den un determinado lugar fisico. Se representa por medio de 
    una matriz"""
    X=list(posx)
    Y=list(posy)
    Tasa_disparo=np.zeros([int(900/bins),int(900/bins)])
    for i in range(disp_clu.shape[0]):
        Tasa_disparo[int(Y[i]/bins)][int(X[i]/bins)]+=1
    return Tasa_disparo

# def Generator_list_fire(dis):
#     if dis != "":
#         llave_1 = dis.index("[", 0)
#         coma = dis.index(",", 0)
#         llave_2 = dis.index("]", 0)
#         try:
#             llave_3 = dis.index("[", llave_1 +1)
#         except ValueError:
#             llave_3 = llave_2
#         x_num = float(dis[llave_1 + 1 : coma])
#         y_num = float(dis[coma + 1 : llave_2])
#         try:
#             return  [ [x_num, y_num] ] + Generator_list_fire(dis[llave_3:])
#         except ValueError:
#             return [ [x_num, y_num] ]
#     else:
#         return []

def Generator_list_fire(dis):
    
    list_to_return = []
    while len(dis) > 4:

        llave_1 = dis.index("[", 0)
        coma = dis.index(",", 0)
        llave_2 = dis.index("]", 0)
        try:
            llave_3 = dis.index("[", llave_1 +1)
        except ValueError:
            llave_3 = llave_2
        x_num = float(dis[llave_1 + 1 : coma])
        y_num = float(dis[coma + 1 : llave_2])
        try:
            list_to_return.append( [x_num, y_num] )
            dis = dis[llave_3:]
        except ValueError:
            return print("vector = ", [ [x_num, y_num] ], "dis = ", dis, len(dis))

    return list_to_return



    
# animal = "jp693"
# date = "0506"
# df = pd.read_csv("/home/tomas_vill/Escritorio/Neuro/{}_{}".format(animal, date))
# list_clu = list(set(df["Clu 1"]))
# df_reduce = df[(df["Clu 1"] == list_clu[0]) & (df["Clu 2"] == list_clu[2])]
# relative_distance = df_reduce["Relative Distance"]
# distances = []
# for i,dist in enumerate(relative_distance):
#     dist = dist[1:-1]
#     distances.append(np.array(Generator_list_fire(dist)))

def Map_shouts(distances, bins = 25.0001):
    """"""
    # Tasa_disparo = np.zeros([int(900/bins),int(900/bins)])
    Tasa_disparo = np.zeros([70,70])
    vector_shouts = distances
    for x, y in vector_shouts:
        if (x >= 0 and y >= 0):
            Tasa_disparo[int(y/bins) + 35][int(x/bins) + 35] += 1
        if (x < 0 and y >= 0):
            Tasa_disparo[int(y/bins) + 35 ][35 + int(x/bins)] +=1
        if (x > 0 and y < 0):
            Tasa_disparo[35 + int(y/bins)][int(x/bins) + 35 ] +=1
        if (x < 0 and y < 0):
            Tasa_disparo[35 + int(y/bins)][35 + int(x/bins) ] +=1
        
    Tasa_disparo = gauss_fil(Tasa_disparo, 1)
    
    return Tasa_disparo

def Map_shouts_no_fillter(distances, bins = 25.0001):
    """"""
    # Tasa_disparo = np.zeros([int(900/bins),int(900/bins)])
    Tasa_disparo = np.zeros([70,70])
    if len(distances)>0:
        for x, y in distances:
            if (x >= 0 and y >= 0):
                Tasa_disparo[int(y/bins) + 35][int(x/bins) + 35] += 1
            if (x < 0 and y >= 0):
                Tasa_disparo[int(y/bins) + 35 ][35 + int(x/bins)] +=1
            if (x > 0 and y < 0):
                Tasa_disparo[35 + int(y/bins)][int(x/bins) + 35 ] +=1
            if (x < 0 and y < 0):
                Tasa_disparo[35 + int(y/bins)][35 + int(x/bins) ] +=1
        
    return Tasa_disparo

def Plotting(distances, animal_date, clu1, clu2, light):
    fig, ax = plt.subplots(2,2, figsize =(25,25))
  #  fig.title(" {} ".format(animal_date, clu1, clu2))
    k=0
    for i in range(2):
        for j in range(2):
            if distances[k].size>0:
                # ax[i,j].plot(distances[k].T[0], distances[k].T[1], "r*")

                ax[i,j].imshow( Map_shouts(distances[k]), cmap = "jet")
                ax[i,j].set_title("{}_Luz {}".format(k, light))
                k += 1
            else:
                ax[i,j].plot([], [], "-*")
                ax[i,j].set_title("{}_Luz {}".format(k, light))
                k += 1
    plt.savefig("/home/tomasg/Escritorio/Neuro/integration/Final_autointegration/img/{}_{}_{}-{}.jpg".format(animal_date, light ,clu1, clu2))
    plt.clf()
    
def Seleccion_Datos(patch = "/home/tomasg/Escritorio/Neuro/integration/Path_integration_cross"):
    """Organizador de graficador"""
    lista_archivos = os.listdir(patch)
    path = []
    for archivo in lista_archivos:
        print(archivo)
        validation = input("Incluir este archivo? Si, cualquier dato, no, dejar vacio")
        if validation != "":
            path.append(archivo)
    print("Usted selecciono los siguientes archivos. Total = ", len(path))
    print(path)
    validation = input("Es correcta la seleccion?")
    if validation != "":
        return path
    else:
        return Main_Organizador()
 # len(distances[:12])>=12
def Make_all_plotting(distances, ruta, clu1, clu2, lights, num_sub_plot = 4):
    dist = distances[: num_sub_plot]
    light = lights[0]
    Plotting(dist, ruta, clu1, clu2, light)
    if len(distances[num_sub_plot:])>=num_sub_plot:
        Make_all_plotting(distances[num_sub_plot:], ruta, clu1, clu2, lights[1:])

def Plotting_prom(matrices, animal_date, clu1, clu2, light):
    fig, ax = plt.subplots(2,2, figsize =(25,25))
  #  fig.title(" {} ".format(animal_date, clu1, clu2))
    k=0
    
    x = [ [arg1,arg2] for arg1 in range(70) for arg2 in range(70) if (35-arg1)**2+(35-arg2)**2<=36]
    x=np.array(x)
    
    
    for i in range(2):
        for j in range(2):
                das=matrices[k].copy()
                das[x.T[0] , x.T[1]] = 0
                ax[i,j].imshow( das, cmap = "jet")
                ax[i,j].set_title("{}_Luz {}".format(k, light))
                k += 1
    plt.savefig("/home/tomasg/Escritorio/Neuro/integration/Path_integration_sin_centro/{}_{}_{}-{}.jpg".format(animal_date, light ,clu1, clu2))
    plt.clf()


def Plotting_unique(matrices, animal_date, clu1, clu2, light):
    """graficar promedio de un unico """
    x = [ [arg1,arg2] for arg1 in range(140) for arg2 in range(140) if (70-arg1)**2+(70-arg2)**2<=25]

    matrices = Mapa_Corr(matrices)
    # x=np.array(x)
    # matrices[x.T[0] , x.T[1]] = 0
    plt.imshow(matrices[40:100,40:100], cmap = "jet")
    plt.title("{} Cluster {}-{} Luz {}".format(animal_date, clu1, clu2, light))
    plt.savefig("/home/tomasg/Escritorio/Neuro/integration/Path_integration_sin_centro_unique_cross/Cr/no_centro/A_{}_{}_{}-{}.jpg".format(animal_date, light ,clu1, clu2))
    plt.clf()
    
def Make_all_plotting_prom(df, animal_date, clu1, clu2, light):
    """Make """
    df_reduce = df[df["Light"]==light[0]]
    
    
    # matrices = [ np.zeros([70,70]) for i in range(4) ]
    # second = np.zeros([70,70])
    # third = np.zeros([70,70])
    # fourth = np.zeros([70,70])
    ###para estar separados en bloques de 30seg
    # for i, dist in enumerate(df_reduce["Relative Distance"]):
    #     matrices[i%4] += Map_shouts_no_fillter(dist)
    # matrices = [gauss_fil(matr/(len(df_reduce)), 1) for matr in matrices]

    
    matrices = np.zeros([70,70])    
    for dist in df_reduce["Relative Distance"]:
         matrices += Map_shouts_no_fillter(dist)
    matrices = gauss_fil(matrices/(len(df_reduce)), 1)
        

    Plotting_unique(matrices, animal_date, clu1, clu2, light[0])
    if len(light)>1:
        Make_all_plotting_prom(df, animal_date, clu1, clu2, light[1:])
    else:
        print("Listo {}_{}".format(animal_date, clu1))
def Main_Organizador():
    path = Seleccion_Datos()
    for ruta in path:
        df = pd.read_csv("/home/tomasg/Escritorio/Neuro/integration/Path_integration_cross/{}".format(ruta))
        list_clu = list(set(df["Clu 1"]))
        for clu1 in list_clu:
            
            list_clu_reduce = list_clu.copy()
            list_clu_reduce.remove(clu1)
            # list_clu_reduce = [clu1]
            for clu2 in list_clu_reduce:
              
                df = pd.read_csv("/home/tomasg/Escritorio/Neuro/integration/Path_integration_cross/{}".format(ruta))
                df.sort_values("Inicio", inplace = True)
                df_reduce = df[(df["Clu 1"] == clu1) & (df["Clu 2"] == clu2)].copy()


                del df
                
                
                
                
                light = df_reduce["Light"].unique().tolist()

                # relative_distance = df_reduce["Relative Distance"] ELIMINAR ESTO

                distances = []
                for i,dist in enumerate(df_reduce["Relative Distance"]):
                    dist = dist[1:-1]
                    distances.append(np.array(Generator_list_fire(dist)))
                df_reduce["Relative Distance"] = distances
                Make_all_plotting_prom(df_reduce, ruta, clu1, clu2, light)
                # Make_all_plotting(distances[:8], ruta, clu1, clu2, light[:2])
                


if __name__ == "__main__":
    
    Main_Organizador()
    
    


