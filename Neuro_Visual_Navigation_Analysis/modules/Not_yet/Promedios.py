#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 20:07:16 2020

@author: tomasg
"""

#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO

import numpy as np
from os import listdir
import pandas as pd
from My_Functions import Cargar
from Dinamica_final import Make_around
###############################################################################################################
#                                           Promediado 1
###############################################################################################################



# dic = pd.read_csv("Similitud_mapa_promediado/" + archivos[0])

def Desmenuzar(nombre):
    """Separa del nombre completo, el nombre del animal, session y cluster"""
    first = nombre.find("_")
    second = nombre.find("_", first+1)
    point = nombre.find(".")
    animal = nombre[:first]
    session = nombre[first + 1 : second]
    cluster = nombre[second + 1:point]
    return animal, session, cluster     

def Agrupar_seccion(df):
    """Agrupa los nombre de archivos por secciones"""
    name_animal = list(set(df["Animal"]))
    dict_sesiones = dict((name, list(set(df[df["Animal"]==name]["Sesiones"]))) for name in name_animal)
    return dict_sesiones

def Carga_df(carpeta = "Similitud_mapa_promediado"):
    archivos = listdir("/home/tomasg/Escritorio/Neuro/Lectura de Datos/{}".format(carpeta))
    archivos = list(filter(lambda arg: arg[-4:]==".csv", archivos))
    archivos_des = list(map(Desmenuzar,archivos))
    archivos_des = np.array(archivos_des)
    df = pd.DataFrame(archivos_des, columns = ["Animal", "Sesiones", "Cluster"])
    df["Ruta"] = archivos
    return df


def Promediando_sesion(datos):
    condiciones = list(set(datos[0]["Luz"] ))
    similitud = []
    luz = []
    incerteza = []
    val = 0
    for cond in condiciones:
        valor = 0
        for i in range(12):
            values = []
            for dataframe in datos:
                df_reduce = list(dataframe["Similitud"][dataframe["Luz"]==cond])
                val = df_reduce[i]
                values.append(val)
            values = np.array(values)
            mean, error = Make_around(values.mean(), values.std() )
            incerteza.append(error)
            similitud.append(mean)
            luz.append(cond)
    return {"Similitud" : similitud, "Incerteza" : incerteza, "Luz" : luz}

def Main_Promedio_seccion(carpeta = "Similitud_mapa_promediado"):
    df = Carga_df(carpeta)
    sesiones = Agrupar_seccion(df)
    for animal in sesiones:
        for sesion in sesiones[animal]:
            df_reduce = df[(df["Sesiones"]==sesion)&(df["Animal"]==animal)]
            datos = [ pd.read_csv(carpeta + "/" + dic) for dic in df_reduce["Ruta"] ]
            promedio = Promediando_sesion(datos)
            df_to_csv = pd.DataFrame(promedio)
            df_to_csv.to_csv(carpeta + "/promedios/" + "{}_{}.csv".format(animal, sesion) )
            
def Promediando_animal(datos):
    similitud = []
    luz = []
    incerteza = []
    val = 0
    type_lights = ["l1", "l2", "l3", "l4", "d1", "d2", "d3", "d4"]
    for cond in range(4):
        for i in range(12):
            values = []
            for dataframe in datos:
                cond_ilu = [ arg  for arg in type_lights if arg in dataframe["Luz"].values] [cond]
                df_reduce = list(dataframe["Similitud"][dataframe["Luz"]==cond_ilu])
                val = df_reduce[i]
                values.append(val)
            values = np.array(values)
            mean, error = Make_around(values.mean(), values.std() )
            incerteza.append(error)
            similitud.append(mean)
            luz.append(cond)
    return {"Similitud" : similitud, "Incerteza" : incerteza, "Luz" : luz}


def Main_Promedio_animal_a(carpeta = "Cros_Corr"):
    df = Carga_df(carpeta)
    sesiones = Agrupar_seccion(df)
    for animal in sesiones:
    
        df_reduce = df[df["Animal"]==animal]
        datos = [ pd.read_csv(carpeta + "/" + dic) for dic in df_reduce["Ruta"] ]
        promedio = Promediando_animal(datos)
        df_to_csv = pd.DataFrame(promedio)
        df_to_csv.to_csv(carpeta + "/promedios_animal/" + "{}_a.csv".format(animal) )


def Promediando_animal_cross(datos):
    similitud = []
    luz = []
    incerteza = []
    val = 0
    type_lights = ["l1", "l2", "l3", "l4", "d1", "d2", "d3", "d4"]
    for cond in range(4):
        for i in range(12):
            values = []
            for dataframe in datos:
                cond_ilu = [ arg  for arg in type_lights if arg in dataframe["Light"].values] [cond]
                # df_reduce = list(dataframe["Similitude"][dataframe["Light"]==cond_ilu])
                cros = list(set(dataframe["Cross_corr"].values))
                for num in range(len(cros)):
                    df_reduce = list(dataframe["Similitude"][(dataframe["Light"]==cond_ilu) & (dataframe["Cross_corr"]==cros[num] )])
                    val = df_reduce[i]
                    values.append(val)
            values = np.array(values)
            mean, error = Make_around(values.mean(), values.std() )
            incerteza.append(error)
            similitud.append(mean)
            luz.append(cond)
    return {"Similitud" : similitud, "Incerteza" : incerteza, "Luz" : luz}
        
def Main_Promedio_animal_cross_a(carpeta = "Cros_Corr"):
    df = Carga_df(carpeta)
    df.drop(["Cluster"], axis = 1, inplace = True)
    sesiones = [an[:-3] for an in df["Sesiones"].values]
    all_animal = list(set(df["Animal"]))
    df["Sesiones"] = sesiones
    
    for animal in all_animal:
    
        df_reduce = df[df["Animal"]==animal]
        datos = [ pd.read_csv(carpeta + "/" + dic) for dic in df_reduce["Ruta"] ]
        promedio = Promediando_animal_cross(datos)
        df_to_csv = pd.DataFrame(promedio)
        df_to_csv.to_csv(carpeta + "/promedios_animal/" + "{}_a.csv".format(animal) )
        
           
        
if __name__ == "__main__":
    Main_Promedio_animal_cross_a()
    print("popo")
    # Main()
