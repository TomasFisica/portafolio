#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 11:49:00 2020

@author: tomasg
"""

#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO


import shutil, os
import imageio as io


# luz = os.listdir("Cros_Corr/Final/jp5519/0610/3_4")
# type_lights = ["l1", "l2", "l3", "l4", "d1", "d2", "d3", "d4"]
# luz = [ light for light in type_lights if light in luz ]
# images = []
# for light in luz:
#     fil_names = os.listdir("Cros_Corr/Final/jp5519/0610/3_4"+"/{}".format(light))
#     fil_names = ordenado(fil_names)
#     for fill in fil_names:
#         images.append(io.imread("Cros_Corr/Final/jp5519/0610/3_4"+"/{}".format(light)+"/"+fill))


def Crear_carpetas(animal, sesion, cros):
    os.makedirs("{}/{}/{}".format(animal, sesion, cros), exist_ok = True)

def Copar_a_destino(animal, sesion, cros,light, kk):
    original = "Cros_Corr/img_cros_cros/{}_{}_{}_{}_{}".format(animal, sesion, cros, kk*10, light)
    name = "{}_{}_{}_{}_{}".format(animal, sesion, cros, kk*10, light)
    destino = "{}/{}/{}/".format(animal, sesion, cros)+name
    shutil.move(original, destino)
    
    
def ordenado(fil_names):
    a = [1,4,5,6,7,8,9,10,11,0,2,3]
    fil_names = sorted(fil_names)
    names = [fil_names[i] for i in a ]
    return names

def Main(ruta = "Cros_Corr/Final/"):
    animal = os.listdir(ruta)
    type_lights = ["l1", "d1", "l2", "d2", "l3", "d3", "l4", "d4"]
    for name in animal:
        sesion = os.listdir(ruta + "{}".format(name))
        path = ruta + "{}/".format(name)
        for date in sesion:
            corr = os.listdir(path + "{}".format(date))
            path_cros = path + "/{}/".format(date) 
            for cros in corr:
                luz = os.listdir(path_cros + "{}".format(cros))
                luz = [ light for light in type_lights if light in luz ]
                images = []
                for light in luz:
                    fil_names = os.listdir(path_cros + "{}".format(cros) +"/{}".format(light))
                    fil_names = ordenado(fil_names)
                    for fill in fil_names:
                        images.append(io.imread(path_cros + "{}".format(cros) +"/{}".format(light) + "/"+fill))
                io.mimsave("Gifs/{}_{}_{}.gif".format(name, date, cros), images, duration = 0.5)


if __name__ == "__main__":
    Main()