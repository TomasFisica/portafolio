#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 19:44:24 2020

@author: tomasg
"""
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from os import listdir

# df = pd.read_csv("threshold_clean/jp693_1006_5.csv")
####################################################################################################################
#                                                       Lectura de tres columnas
####################################################################################################################
def Sorted_light(light):
    
    # luz = [ luz for luz in ["l1", "l2", "l3", "l4"] if luz in light ]
    # dark = [ luz for luz in ["d1", "d2", "d3", "d4"] if luz in light ]
    luz = [ luz for luz in [0, 1] if luz in light ]
    dark = [ luz for luz in [2, 3] if luz in light ]
    finally_light = []
    for num in range(len(light)):
        try:
            finally_light.append(luz[num])
            finally_light.append(dark[num])
        except:
            break
    return finally_light

def Graphic(df, name_fig, path):
    
    comun_rangex = list(range(1,13,1))
    light = list( set(df["Luz"]) )
    light = Sorted_light(light)
    y = []
    erry = []
    for li in light:
        y.append(df[df["Luz"]==li])
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(1,4,sharey=True)
    for i, ax in enumerate([ax1, ax2, ax3, ax4]):
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.grid(True)
        ax.errorbar( comun_rangex, y[i]["Similitud"], yerr = y[i]["Incerteza"], fmt =".", capsize = 4, ecolor = "r" )
        ax.set_xlabel(str(y[i]["Luz"][0:1].values[0]))
        ax.set_xticks(range(2,14,2))
    for ax in [ax2, ax3, ax4]:
        ax.spines["left"].set_visible(False)
    fig.suptitle(name_fig[:-4])
    plt.savefig(path[:-4]+".jpg")
    plt.clf()
    plt.close()
    # plt.show()
    
def Graficador(paths = ["None"] ,folder = "Cros_Corr/promedios_animal", listas = []):
    
    try:
        if paths[0]=="None":
            listas =listdir(folder)
            expandir = lambda arg: folder+"/"+arg
            paths = list(map(expandir, listas))
    except:
        print("Listo")
    if len(paths)>=1:
        df = pd.read_csv(paths[0])
        Graphic(df, listas[0], paths[0])
        return Graficador(paths = paths[1:], folder = folder, listas = listas[1:])

def Graficador_cross(paths = ["None"] ,folder = "Cros_Corr/promedios_animal"):
    try:
        if paths[0]=="None":
            listas =listdir(folder)
            expandir = lambda arg: folder+"/"+arg
            paths = list(map(expandir, listas))
    except:
        print("Listo")
    if len(paths)>=1:
      df = pd.read_csv(paths[0])
      cluster_cros = list(set(df["Cross_corr"]))
      for clu_cro in cluster_cros:
          df_clu = df[df["Cross_corr"] == clu_cro]
          df_clu.rename(columns = {"Light":"Luz", "Similitude":"Similitud"}, inplace = True)
          animal, date, cross = [df_clu["Animal"].values[0], df_clu["Date"].values[0], df_clu["Cross_corr"].values[0]]
          df_clu.insert(column ="Incerteza",  value=[0.0]*48, loc=5)
          df_clu = df_clu[["Incerteza", "Luz", "Similitud"]]
          name_fig = "{}_{}_{}.csv".format(animal, date, cross)
          path = folder+"/"+name_fig 
          Graphic(df_clu, name_fig, path)
      return Graficador_cross(paths = paths[1:], folder = folder)
Graficador()


#                         print("kk", kk)
#                         print("cross", len(cross_corr))
#                         print("main", len(main_average))
#                         print("simil", len(simil))
#                         print("{}_{}_{}_{}".format(animal, date,light,etiquetas[i]))

####################################################################################################################
#                                                       Lectura de cros cor 
####################################################################################################################
# ruta = "Cros_Corr"
# df = pd.read_csv("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Cros_Corr/jp693_1206.csv")
# cluster_cros = list(set(df["Cross_corr"]))
# df_clu = df[df["Cross_corr"] == cluster_cros[0]]
# df_clu.rename(columns = {"Light":"Luz", "Similitude":"Similitud"}, inplace = True)
# animal, date, cross = [df_clu["Animal"].values[0], df_clu["Date"].values[0], df_clu["Cross_corr"].values[0]]
# df_clu.insert(column ="Incerteza",  value=[0.0]*48, loc=5)
# df_clu = df_clu[["Incerteza", "Luz", "Similitud"]]
# name_fig = "{}_{}_{}.csv".format(animal, date, cross)
# path = ruta+"/"+name_fig

# Graficador_cross()

