#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO

import pickle


def Cargar(name):
    """Cargar archivos"""
    with open (name, "rb") as hand:
        dic=pickle.load(hand)
    return dic

if __name__=="__main__":
    print("Ejecutado manualmente")