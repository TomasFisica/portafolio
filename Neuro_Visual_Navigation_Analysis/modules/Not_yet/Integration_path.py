#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 15:20:37 2020

@author: tomas_vill
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot
import pickle
import os
def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic


def Define_interval_trials(dic):
    """Devuelve un DF con los intervalos"""
    intervals = pd.DataFrame(dic["Light_Trials"], columns= ["Number Trial", "Type_light", "Start", "End"]).set_index("Number Trial")
    intervals["Start"] = intervals["Start"].astype(int)
    return intervals


def Sub_intervals_trial(intervals, size_windwos = 30):
    """Funcion que retorno yield con los sub intervalos maximos y minimo """
    if type(intervals) == pd.DataFrame:
        start = int(intervals["Start"])
    elif type(intervals) == int:
        start = intervals
    else:
        print("No cargaste ni un DataFrame ni un entero para definir el inico")
        exit
    size_windwos *= 20000
    for i in range(4):
        if i !=3 :
            yield [start, start + size_windwos]
        else:
            yield [start, start + size_windwos - 10*20000]
        start += size_windwos
        
def Sub_intervals_trial_second(intervals, size_windwos = 30):
    """Funcion que retorno yield con los sub intervalos maximos y minimo. Para todos los trials """
    if type(intervals) == pd.DataFrame:
        start = int(intervals["Start"])
    elif type(intervals) == int:
        start = intervals
    else:
        print("No cargaste ni un DataFrame ni un entero para definir el inico")
        exit
    size_windwos *= 20000
    i = 0
    while i<240: # 60 trials x 4 sub_interval_trials
        
        if i%3 !=3 :
            yield [start, start + size_windwos]
        else:
            yield [start, start + size_windwos - 10*20000]
        i += 1
        start += size_windwos        

def Aux_Generator_spike(lista):
    """Auxiliar function """
    spikes =[]
    for val in lista:
        spikes += list(val)
    return spikes

def Generator_spike_train(dic, i):
    """Devuelve una lista con todos los spikes"""
    luces = ["Luz", "Oscuridad"]
    spikes = []
    for ligh in luces:
        keys_ligh = dic["Cluster Numero {}".format(i)][ligh].keys()
        primer_orden = [dic["Cluster Numero {}".format(i)][ligh][key] for key in keys_ligh]
        primer_orden = Aux_Generator_spike(primer_orden)  
        spikes += primer_orden
    spikes.sort()
    df = pd.Series(spikes)
    return df

def Aux_in_windows(clu, trains_spikes, interval):
    sp_principal = trains_spikes["{}".format(clu)]
    sp_principal = sp_principal[(sp_principal>=interval[0])&(sp_principal<interval[1])]
    return sp_principal
    
def Aux_Relative_distance(positions, spike, spike_b):
    """Reurn relative positions to a spkie"""
    principal_psition = positions[int(spike/400)]
    spike_b = [ int(arg/400) for arg in spike_b ]
    secondary_positions = positions[spike_b]
    relative_distance = [ [arg[0] - principal_psition[0], arg[1] - principal_psition[1]] for arg in secondary_positions]
    return relative_distance

def Generate_relative_distance(clu, clu_b, trains_spikes, interval, positions, size_windows_b = 10):
    """Reurn all relative positions"""
    spike_a_in_principal_windows = Aux_in_windows(clu, trains_spikes, interval)  
    relative_distance = []
    for spike in spike_a_in_principal_windows:
        spike_b = Aux_in_windows(clu_b, trains_spikes, [spike, spike + 20000*size_windows_b]) 
        relative_distance += Aux_Relative_distance(positions, spike, spike_b)
    return relative_distance
    

def Driving_sp_A(animal, date, lista_clu = []):
    dic = Cargar("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/{}/Diccionario_{}".format(animal, date))
    positions = dic["Posicion"]
    trains_spikes = { "Cluster {}".format(i): Generator_spike_train(dic, i) for i in lista_clu }
    intervals = Define_interval_trials(dic)  
    
    clu_principal = []
    clu_secundario = []
    lights = []
    relative_distance = []
    interval_start = []
    interval_finish =[]
    for clu in trains_spikes:
        # other_clu = [arg for arg in trains_spikes if arg!=clu]
        other_clu = [clu]
        for light, start, _ in intervals.values:
            sub_interval = Sub_intervals_trial(start)
            for interval in sub_interval:
                for clu_b in other_clu:    
                    relativedistance = Generate_relative_distance(clu, clu_b, trains_spikes, interval, positions) 
                    relative_distance.append(relativedistance)
                    clu_principal.append(clu)
                    clu_secundario.append(clu_b)
                    lights.append(light)
                    interval_start.append(interval[0])
                    interval_finish.append(interval[1])
    df = pd.DataFrame({"Clu 1" : clu_principal, "Clu 2" : clu_secundario, "Relative Distance" : relative_distance, "Light": lights, "Inicio" : interval_start, "Final":interval_finish})
    df.to_csv("/home/tomasg/Escritorio/Neuro/integration/Final_autointegration/{}_{}".format(animal,date))
    print("Creado archivo del animal {}_{}".format(animal, date))

def Driving_sp_A_second(animal, date, lista_clu = []):
    dic = Cargar("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/{}/Diccionario_{}".format(animal, date))
    positions = dic["Posicion"]
    trains_spikes = { "Cluster {}".format(i): Generator_spike_train(dic, i) for i in lista_clu }
    
    intervals = Define_interval_trials(dic)  
    light_were_used = intervals["Type_light"].unique()
    
    clu_principal = []
    clu_secundario = []
    lights = []
    relative_distance = []
    interval_start = []
    interval_finish =[]
    for clu in trains_spikes:
        # other_clu = [arg for arg in trains_spikes if arg!=clu]
        other_clu = [ arg for arg in trains_spikes if arg != clu]
        for l_or_d in light_were_used:
            for light, start, _ in intervals[intervals["Type_light"] == l_or_d ].values:        
                sub_interval = Sub_intervals_trial(start)
                for interval in sub_interval:
                    for clu_b in other_clu:    
                        relativedistance = Generate_relative_distance(clu, clu_b, trains_spikes, interval, positions) 
                        relative_distance.append(relativedistance)
                        clu_principal.append(clu)
                        clu_secundario.append(clu_b)
                        lights.append(light)
                        interval_start.append(interval[0])
                        interval_finish.append(interval[1])
    df = pd.DataFrame({"Clu 1" : clu_principal, "Clu 2" : clu_secundario, "Relative Distance" : relative_distance, "Light": lights, "Inicio" : interval_start, "Final":interval_finish})
    df.to_csv("/home/tomasg/Escritorio/Neuro/integration/Path_integration_cross/{}_{}".format(animal,date))
    print("Creado archivo del animal {}_{}".format(animal, date))


def Main_function(datos):
    """Principal function """
    print("Iniciando funcion principal")
    for animal in datos:
        for date in datos[animal]:
            Driving_sp_A_second(animal, date, datos[animal][date])
    print("Fin de funcion principal")
    
if __name__ == "__main__":
    inicio = os.times()[4]
    datos = {"jp693":{"0506":[9,10,12],"1006":[5,12],"1106":[5, 6, 7, 17],
                          "1206":[2, 4, 5, 6, 13] }, "jp5519":{"0610":[2, 3, 4],
                          "0810":[2, 3, 4, 6, 8, 9],"0910":[2, 3, 5],"1010":[2, 4, 5],"1110":[2, 3, 5],
                        "1210":[3, 6, 7],"1510":[3, 4, 5, 6]} }
    # datos = {"jp693":{"0506":[9,10,12],"1006":[5,12] } }
    a = Main_function(datos)
    
    fin = os.times()[4]
    total = fin - inicio
    horas = int(total/(60*60 ))
    total = total -horas*60*60
    minutos = int(total/60)
    segundos = round(total - minutos*60, 2)
    print("El programa tardo {} horas, {} minutos y {} segundos.".format(horas, minutos, segundos))