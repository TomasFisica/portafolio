#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 18:39:29 2020

@author: tomasg
"""

#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO


import sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.ndimage import gaussian_filter as gauss_fil
from os import listdir
import pandas as pd
import pickle
from My_Functions import *
from Dinamica_evolituva import *
import time


def Intervals_trial(dic, light):
    """Return a matrix with the start and end values of the "trials """
    values_times = dic["Light_Trials"][np.where(dic["Light_Trials"][:,1] == light)][:,2:]
    start_end_trial = [ [time[0], time[1]] for time in values_times   ]
    return start_end_trial[:11]

def Return_map_rate_trial(dic, num_clu, start_end_trial, time_axis, bins = 25.0001):
    """Return the sum of all map rate with values in windows"""
    time_spike_sort = Return_time_spike_sort(num_clu, dic)
    map_rate = np.zeros([int(900/bins),int(900/bins)])
    for start, end in start_end_trial:
        windows = [int(start), int(end)]
        spike = Cutout_spike(time_spike_sort, windows)
        map_rate += Map_Rate(spike, dic["Posicion"], windows)
    return map_rate/len(start_end_trial)

def Time_Axis(dic):
    """Return de time axis"""
    val=dic["Posicion"].T.shape[1]
    Eje_Temporal = [400*(i+1) for i in range(val)]
    return np.array(Eje_Temporal)

def Average_trials(dic, light, num_clu):
    """Return the average of all trials """
    start_end_trial = Intervals_trial(dic, light)
    map_average = np.zeros([])
    time_axis = Time_Axis(dic)
    map_average = Return_map_rate_trial(dic, num_clu, start_end_trial, time_axis)
    map_average = gauss_fil(map_average, 1)
    return map_average

def Make_around(mean, std):
    """Return de mean value and its error"""
    j = 0
    for i in str(std)[2:]:
        j += 1
        if i != "0":
            break
    return np.around(mean, j), np.around(std, j)

def Clean_matrix(first, second):
    first = np.take(first, np.where(second!=0)).flatten()
    second = np.take(second, np.where(second!=0)).flatten()
    second = np.take(second, np.where(first!=0)).flatten()
    first = np.take(first, np.where(first!=0)).flatten()
    return first, second

def Calculate_similitude(first, rate_maps):
    """Calculate similitude"""
    values = []
    # for matrix in rate_maps:
    #     da=first.copy()
    #     da, ma = Eliminar_nan(da, matrix)
    #     da, ma = Eliminar_zeros(da, ma)
    #     # da[da>=0.2]=1
    #     # da[da<0.2]=0
    #     # ma[ma>=0.2]=1
    #     # ma[ma<0.2]=0
    #     values.append(np.corrcoef(da.T, ma.T)[0][1])
    # values = np.array([ np.corrcoef(first.flatten(), matrix.flatten())[0][1] for matrix in rate_maps])
    # values = np.array(values)
    # values = values[~np.isnan(values)]
    # mean, error = Make_around(values.mean(), values.std() )
    
    
###### con Calculate_partial_maps_rate_three
    da, ma = Eliminar_nan(first, rate_maps)
    da, ma = Eliminar_zeros(da, ma)
    values = np.corrcoef(da.T, ma.T)[0][1]
    mean=values
    error = 0.0
    return [mean, error]

# def Calculate_similitude(first, rate_maps):
#     """Calculate similitude"""
#     values = []
#     ver = np.zeros_like(first)
#     for matrix in rate_maps:
#         ver +=matrix
#     ver /=len(rate_maps)
#     da, ma = Eliminar_nan(first, ver)
#         # da[da>=0.2]=1
#         # da[da<0.2]=0
#         # ma[ma>=0.2]=1
#         # ma[ma<0.2]=0
#     values = np.corrcoef(da, ma)[0][1]
#     # values = np.array([ np.corrcoef(first.flatten(), matrix.flatten())[0][1] for matrix in rate_maps])
#     # values = np.array(values)
#     # values = values[~np.isnan(values)]
#     mean, error = Make_around(values, 0.01 )
#     return [mean, error]


def Calculate_Score(matrix):
    """DESAHBILITADA MOMENTANEAMENTE"""
    autocorr = Mapa_Corr(matrix)
    grid_score = Calculo_grid_not_origin_extern_radios_variables(autocorr)
    return grid_score

def Calculate_grid_score(rate_maps):
    """Calculate grid score """
    values = np.array( [ Calculate_Score(matrix) for matrix in rate_maps ] )
    mean, error = Make_around(values.mean(), values.std() )
    return [mean, error]

def Aux_func_Calculate_autocorr(first, matrix):
    first, matrix = Eliminar_nan(first, matrix)
    return matrix
    

def Calculate_similitude_autocor(first, rate_maps):
    """Calculate similitude buy with autocorr_maps"""
    first = Mapa_Corr(first)
    mapa_corr = lambda matrix: Mapa_Corr(matrix, 1)
    auto_corr_maps = list(map(mapa_corr, rate_maps))
    # aux_func = lambda matrix : Aux_func_Calculate_autocorr(first, matrix)
    # auto_corr_maps = list(map(aux_func, auto_corr_maps))
    mean, error = Calculate_similitude(first, auto_corr_maps)
    return [mean, error]
###### 
    
def Map_Rate_second(spike, position, windows):
    """This funcion return a rate-spike mape"""
    map_time = Map_Time(position, windows)
    vector_shouts = Vector_shouts(spike)
    map_shouts = Map_shouts(vector_shouts, position)
    rate = Rate_second(map_shouts, map_time)
    return rate

def Map_Rate_three(spike, position, windows):
    """Tercera opcion. sumo todo"""
    map_time = Map_Time(position, windows)
    vector_shouts = Vector_shouts(spike)
    map_shouts = Map_shouts(vector_shouts, position)
    return map_time, map_shouts


def Rate_second(map_shouts, map_time):
    
    division = map_shouts/map_time
    return division
    

def Calculate_partial_maps_rate(dic, light, num_clu, overlap = 0, size_windows = 10):
    """Devuelve los matrices l1[:10], l2[:10] ... correspondientes los triales de la misma luz"""        
    start_end_trial = np.array(Intervals_trial(dic, light), dtype = int )
    start_end_trial[:,1] = start_end_trial[:,0] + size_windows*20000  #with this I create a windows that have a 10se of size
    # time_axis = Time_Axis(dic)
    if overlap != 0:
        num_steps = int((120 - size_windows)/overlap + 1)
    else:
        num_steps = int(120/size_windows)
        overlap = size_windows
    time_spike_sort = Return_time_spike_sort(num_clu, dic)
    Cut_Spike = lambda windows : Cutout_spike(time_spike_sort, windows)
    Rate_maps = lambda spike, windows : Map_Rate_second(spike, dic["Posicion"], windows)
    for step in range(num_steps):
        # Put here the code
        spikes = list(map(Cut_Spike,start_end_trial)) 
        map_rate = list(map( Rate_maps, spikes, start_end_trial))
        
        start_end_trial[:,1] = start_end_trial[:,1] + overlap*20000
        start_end_trial[:,0] = start_end_trial[:,0] + overlap*20000
        yield map_rate 
      

def Calculate_partial_maps_rate_three(dic, light, num_clu, overlap = 0, size_windows = 10):
    """Devuelve una matriz promediada de todas las condiciones para la misma ventana"""        
    start_end_trial = np.array(Intervals_trial(dic, light), dtype = int )
    start_end_trial[:,1] = start_end_trial[:,0] + size_windows*20000  #with this I create a windows that have a 10se of size
    # time_axis = Time_Axis(dic)
    if overlap != 0:
        num_steps = int((120 - size_windows)/overlap + 1)
    else:
        num_steps = int(120/size_windows)
        overlap = size_windows
    time_spike_sort = Return_time_spike_sort(num_clu, dic)
    Cut_Spike = lambda windows : Cutout_spike(time_spike_sort, windows)
    Rate_maps = lambda spike, windows : Map_Rate_three(spike, dic["Posicion"], windows)
    for step in range(num_steps):
        # Put here the code
        spikes = list(map(Cut_Spike,start_end_trial)) 
        maps_totales = list(map( Rate_maps, spikes, start_end_trial))
        map_time = np.zeros_like(maps_totales[0][0])
        map_shouts = np.zeros_like(maps_totales[0][0])
        for time, shouts in maps_totales:
            map_time += time
            map_shouts += shouts
        map_rate = Rate(map_shouts, map_time)
        map_rate = gauss_fil(map_rate, 1)
        start_end_trial[:,1] = start_end_trial[:,1] + overlap*20000
        start_end_trial[:,0] = start_end_trial[:,0] + overlap*20000
        yield map_rate 
  


def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic


def Similitude(num_clu, dic):
    
    # dic = Cargar(direction)
    type_lights = ["l1", "l2", "l3", "l4", "d1", "d2", "d3", "d4"]
    type_lights = [light for light in type_lights if light in dic["Light_Trials"][:,1]]
    average_light = Average_trials(dic, type_lights[0], num_clu)
    map_rate = np.zeros([])
    val = []
    error = []
    list_light = []
    for light in type_lights:
        cluster = Calculate_partial_maps_rate_three(dic, light, num_clu)
        while True:
            try:            
                map_rate = cluster.__next__()
                retorn = Calculate_similitude(average_light, map_rate)
                val.append(retorn[0])
                error.append(retorn[1])
                list_light.append(light)
            except:
                break
    dic_return = {"Cluster":[num_clu]*len(val), "Similitud":val, "Incerteza":error, "Luz" : list_light}
    return dic_return    

def Main_similitude(direcciones):
    """Generate all csv. with the evolition of correlation """
    ruta = "/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/{}/Diccionario_{}"
    for animal in direcciones:
        for date in direcciones[animal]:
            dic = Cargar(ruta.format(animal, date))
            for num_clu in direcciones[animal][date]:
                to_save = pd.DataFrame(Similitude(num_clu, dic))
                to_save.to_csv("ultimaaed/{}_{}_{}.csv".format(animal, date, num_clu), index = False)
                


def Organizador(matrices, funcion):
    """Organiza los procesos"""
    list_to_return = []
    for first in range(len(matrices)):
        for second in range(first+1,len(matrices)):
            list_to_return.append(funcion(matrices[first], matrices[second]))
    return list_to_return
    
def Etiquetador(first, second):
    return "{}_{}".format(first, second)


# def Main_similitude_cross(direcciones):
#     """Generate all csv. with the evolition of correlation """
#     ruta = "/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/{}/Diccionario_{}"
#     for animal in direcciones:
#         for date in direcciones[animal]:
#             dic = Cargar(ruta.format(animal, date))
#             clusteres = direcciones[animal][date]
#             type_lights = ["l1", "l2", "l3", "l4", "d1", "d2", "d3", "d4"]
#             type_lights = [light for light in type_lights if light in dic["Light_Trials"][:,1]]
#             main_average = [Average_trials(dic, type_lights[0], num_clu) for num_clu in clusteres]
#             main_average = Organizador(main_average, Mapa_Cross_Corr)
            
             
#             etiquetas = Organizador(clusteres, Etiquetador)
            
#             csv_animal = []
#             csv_date = []
#             csv_cross_corr = []
#             csv_similitud = []
#             csv_light = []            
            
#             for light in type_lights:
#                 clusters = [Calculate_partial_maps_rate_three(dic, light, num_clu) for num_clu in clusteres]
#                 kk=0
#                 while True:
#                     kk+=1
#                     try:
#                         map_rate = [clu.__next__() for clu in clusters]
#                         cross_corr = Organizador(map_rate, Mapa_Cross_Corr)
#                         Calc_simil = lambda arg1, arg2: Calculate_similitude(arg1, arg2)[0]
#                         simil = list(map(Calc_simil, main_average, cross_corr ) )
#                         for i in range(len( etiquetas)):
#                             csv_animal.append(animal)
#                             csv_date.append(date)
#                             csv_cross_corr.append(etiquetas[i])
#                             csv_similitud.append(simil[i])
#                             csv_light.append(light)
#                     except StopIteration:
#                         break
                    
#             dic_to_csv = {"Animal": csv_animal, "Date": csv_date, "Cross_corr" : csv_cross_corr, "Similitude": csv_similitud, "Light" : csv_light}
#             dic_to_csv = pd.DataFrame(dic_to_csv)
#             dic_to_csv.to_csv("Cros_Corrr/New_{}_{}.csv".format(animal, date), index = False)
         

         







def Main_similitude_cross(direcciones):
    """Generate all csv. with the evolition of correlation SIMPLEMENTE CREO LAS IMAGENES """
    ruta = "/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/{}/Diccionario_{}"
    for animal in direcciones:
        for date in direcciones[animal]:
            dic = Cargar(ruta.format(animal, date))
            clusteres = direcciones[animal][date]
            type_lights = ["l1", "l2", "l3", "l4", "d1", "d2", "d3", "d4"]
            type_lights = [light for light in type_lights if light in dic["Light_Trials"][:,1]]
            # main_average = [Average_trials(dic, type_lights[0], num_clu) for num_clu in clusteres]
            # main_average = Organizador(main_average, Mapa_Cross_Corr)
            
             
            etiquetas = Organizador(clusteres, Etiquetador)
            
            csv_animal = []
            csv_date = []
            csv_cross_corr = []
            csv_similitud = []
            csv_light = []            
            
            for light in type_lights:
                # clusters = [Calculate_partial_maps_rate_three(dic, light, num_clu) for num_clu in clusteres]
                kk=0
                while True:
                    kk+=1
                    try:
                        # map_rate = [clu.__next__() for clu in clusters]
                        # cross_corr = Organizador(map_rate, Mapa_Cross_Corr)
                       
                        for i in range(len( etiquetas)):
                            # plt.imshow(cross_corr[i], cmap="jet")
                            # plt.title("{}_{}_{}_{}_{}".format(animal, date, etiquetas[i], kk, light))
                            # plt.savefig("Cros_Corr/img_cros_cros/{}_{}_{}_{}_{}".format(animal, date, etiquetas[i], kk*10, light))
                            # plt.clf()
                            Crear_carpetas(animal, date, etiquetas[i], light)
                            Mover_a_destino(animal, date, etiquetas[i], light, kk)
                    except StopIteration:
                        break
                    if kk==12:
                        break
                             
import shutil, os

def Crear_carpetas(animal, sesion, cros, light):
    os.makedirs("Final/{}/{}/{}/{}".format(animal, sesion, cros, light), exist_ok = True)

def Mover_a_destino(animal, sesion, cros,light, kk):
    original = "Cros_Corr/img_cros_cros/{}_{}_{}_{}_{}.png".format(animal, sesion, cros, kk*10, light)
    name = "{}_{}_{}_{}_{}".format(animal, sesion, cros, kk*10, light)
    destino = "Final/{}/{}/{}/{}".format(animal, sesion, cros,light)
    shutil.copy(original, destino)
      









                      
if __name__=="__main__" :    
    inicio = time.time()
    direccion = {"jp693":{"1006":[5,12], "1106":[5,6,7,17], "1206":[2,4,5,6,13]},
                  "jp5519": {"0610":[2,3,4], "0810":[2,3,4,6,8,9], "0910":[2,3,5], "1010":[2,4,5], "1110":[2,3,5], "1210":[3,6,7,14,15], "1510":[3,4,5,6,7,8] }
                }
    # Main_similitude(direccion)
    Main_similitude_cross(direccion)
    fin=time.time()
    time_transcurrido=fin-inicio
    minutos=int(time_transcurrido/60)
    seg=round(time_transcurrido-minutos*60,1)
    print("El programa tardo ", minutos, " minutos y ", seg, " segundos.")

