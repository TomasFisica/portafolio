#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO

#This lib give to the software the principal graphical interface
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import Label, Frame, Button, Image, Tk, Entry, StringVar, Checkbutton, IntVar, messagebox, BooleanVar
from tkinter import PhotoImage
from tkinter.ttk import Combobox

import modules.Basic as Basic
import modules.Analysis as Analysis
################################################################################
 #                               First windows
################################################################################ 


def Top():
    top = Tk()
    top.title("Nuero Visual 1.0")
    Button
    Exit_buttom = Button(top , text = "Exit", command = top.destroy )
    Exit_buttom.grid(row = 4, column = 4)
    Start_buttom = Button(top, text = "Start", command = lambda : Change_windows(top) )
    Start_buttom.grid(row = 4, column = 2)

    Label
    Welcome = Label(top, text =" Welcome to Neuro Visual Navigation")
    Welcome.grid(row = 1, column = 2)
    Info_1 = Label(top,    text = "Remember to read the 'Readme' file if you have")
    Info_1.grid(row = 2, column = 1)
    Info_2 = Label(top,    text = "questions about the operation of the software ")
    Info_2.grid(row = 3, column = 1)
    top.mainloop()

def Change_windows(top):
    root_2 = Tk()
    top.destroy()
    second = Second(master = root_2)
    second.mainloop()


################################################################################
  #                              Second windows
################################################################################

class Diccionario:
    
    def __init__(self, path):
        self.path = path
        self.dic = self.Upload_dic()
        self.list_cluster = self.Update_Cluster()
        self.time_axis = self.Upload_Time_Axis()
        self.clu_1 = None
        self.clu_2 = None
        
    def Upload_Time_Axis(self):
        """ Create a temporal axies  """
        time_axis = np.zeros(self.dic["Posicion"].T.shape[1])
        for i in range(time_axis.shape[0]):
            time_axis[i]=400*(i+1)   
        return time_axis

    def Upload_clu(self, num, clu):
        if num == 1:
            self.clu_1 = clu
        else:
            self.clu_2 = clu
    def Upload_dic (self):
       """ upload the principal dictionary  """
       return Basic.Cargar(self.path)
    
    def Update_Cluster(self):
        """ create a list with the name of all cluster in the dictionary """
        keys = self.dic.keys()
        list_clu = [arg for arg in keys if (arg[:4] == "Clus") & ((~(arg[-1:] in ["0","1"])) | ((arg[-2:] in ["10","11"])) )  ]
        return list_clu


class Second(Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.master.geometry("750x500")
        self.master.title("Neuro Visual Navigation 1.0 - in operation")
        
        self.__int_cross_cor = BooleanVar(self.master)         # crros corr 1, autocorr 0
        self.string_path = StringVar(self.master)          # path where is the file to load
        self.string_luz = StringVar(self.master)
        self.string_type_luz = StringVar(self.master)
        self.boolead_path = BooleanVar(self.master)
        self.diccionario = {}



        self.Create_widgets()


    def Create_widgets(self):

                                # Label
        self.welcome = Label(self.master, text = """Para iniciar, indicar la ubicación del 
        archivo y su extensión""", width = 30, height = 2)
        self.welcome.grid(row = 0, column = 0)
        self.ubicacion = Label(self.master, text = "Ubicación" )
        self.ubicacion.grid(row = 1, column = 0)

        self.label_cluster1 = Label(self.master, text  = "Cluster 1")
        self.label_cluster1.grid(row = 2, column = 0)
        self.label_cluster2 = Label(self.master, text  = "Cluster 2")
        self.label_cluster2.grid(row = 3, column = 0)
        self.label_type_file = Label(self.master, text  = "Tipo de archivo")
        self.label_type_file.grid(row = 1, column = 2)
        self.label_type_analysis = Label(self.master, text = "Tipo de análisis")
        self.label_type_analysis.grid(row = 4, column = 0)
        self.label_grid_score = Label (self.master, text = "")
        self.label_grid_score.grid(row = 5, column = 0)
        self.label_luz = Label(self.master, text = "Luz")
        self.label_luz.grid(row = 5, column = 1)
        self.label_type_luz = Label(self.master, text = "Tipo Luz")
        self.label_type_luz.grid(row = 5, column = 3 )

                                # Entry
        self.entry_ubicacion = Entry(self.master, textvariable = self.string_path )
        self.entry_ubicacion.grid(row =1, column = 1)
        self.entry_luz = Entry(self.master, textvariable = self.string_luz)
        self.entry_luz.grid(row = 5, column = 2)
        self.entry_type_luz = Entry(self.master, textvariable = self.string_type_luz)
        self.entry_type_luz.grid(row= 5, column = 4)

                                # Combobox
        self.combo_cluster1 = Combobox(self.master, values = None,
            state = "disabled")
        self.combo_cluster1.grid(row = 2, column = 1)
        self.combo_cluster2 = Combobox(self.master, values = self.combo_cluster1["values"], state = "disabled")
        self.combo_cluster2.grid(row = 3, column = 1)
        self.combo_type_file = Combobox(self.master, values = ["Diccionario","csv", "xls"] , state = "readonly")
        self.combo_type_file.grid(row = 1, column = 3)
        self.combo_type_analysis = Combobox(self.master, values = ["Mapa de disparo", "Autocorrelación", "Correlación cruzada",
                                    "Mapa de similitud", "Mapa evocado por disparo" , "Grid Score"], state = "disabled")
        self.combo_type_analysis.grid(row = 4, column = 1)
        self.combo_type_analysis.bind("<<ComboboxSelected>>", lambda _ : self.combo_type_analysis_selected())

        
        
                                # Checkbox

      

                                # Button
        
        self.button_validation_path = Button(self.master, text = "Validar path", 
                command = self.Validation_path )
        self.button_validation_path.grid(row = 1, column = 4)
        self.button_make_analysis = Button(self.master, text = "Realizar Análisis", state = "disabled",
                command = self.Make_Analysis)
        self.button_make_analysis.grid(row = 4, column = 2)

                                ## Functions  ##
    def Make_Analysis(self):
        Analysis = { "Grid Score" : self.Grid_Score, "Mapa de disparo" : self.Tasa_Disparo,
        "Autocorrelación" : self.Mapa_Correlacion, "Correlación cruzada" : self.Mapa_Correlacion_Cruzada    }
        type_analysis = str(self.combo_type_analysis.get())
        Analysis[type_analysis]()
        
    def Tasa_Disparo(self):
        clu = self.combo_cluster1.get().replace("Cluster Numero ", "")
        luz = self.string_luz.get()
        type_luz = self.string_type_luz.get()
        tasa, _ = Analysis.Cluster_type_light_(self.diccionario.dic,luz,type_luz,clu)
        self.Show_Image(tasa, self.master, 6,4)
    
    def Mapa_Correlacion(self):
        clu_1 = self.combo_cluster1.get().replace("Cluster Numero ", "")
        luz = self.string_luz.get()
        type_luz = self.string_type_luz.get()
        _ , tasa_1 = Analysis.Cluster_type_light_(self.diccionario.dic,luz,type_luz,clu_1)
        correlacion, _ = Analysis.Mapa_Corr(tasa_1)
        self.Show_Image(correlacion, self.master, 6, 4)
        
    def Mapa_Correlacion_Cruzada(self):
        clu_1 = self.combo_cluster1.get().replace("Cluster Numero ", "")
        clu_2 = self.combo_cluster2.get().replace("Cluster Numero ", "")
        luz = self.string_luz.get()
        type_luz = self.string_type_luz.get()
        _ , tasa_1 = Analysis.Cluster_type_light_(self.diccionario.dic,luz,type_luz,clu_1)
        _ , tasa_2 = Analysis.Cluster_type_light_(self.diccionario.dic,luz,type_luz,clu_2)
        correlacion_cruzada, _ = Analysis.Mapa_Cross_Corr(tasa_1, tasa_2)
        self.Show_Image(correlacion_cruzada,self.master, 6, 4)

    def Grid_Score(self):

        clu = self.combo_cluster1.get().replace("Cluster Numero ", "")
        luz = self.string_luz.get()
        type_luz = self.string_type_luz.get()
        _ , tasa_1 = Analysis.Cluster_type_light_(self.diccionario.dic,luz,type_luz,clu)
        _, correlacion = Analysis.Mapa_Corr(tasa_1)
        gridscore, fig = Analysis.Calculo_grid_not_origin_extern_radios_variables(correlacion)
        gridscore = np.round(gridscore,2)
        self.label_grid_score["text"] = "El valor de Grid Score es {}".format(gridscore)
        self.Show_Image(fig, self.master, 6, 4)

    def Show_Image(self, figure, master_value, x_grid = 0, y_grid = 0  ):
        canvas = FigureCanvasTkAgg(figure, master = master_value)
        canvas.get_tk_widget().grid(row = x_grid, column = y_grid)

    def combo_type_analysis_selected(self):
      if self.combo_type_analysis.get() in ["Correlación cruzada", "Mapa evocado por disparo"]:
         self.combo_cluster2["state"] = "normal"
         self.button_make_analysis["state"] = "normal"
      else:
         self.combo_cluster2["state"] = "disabled"
         self.button_make_analysis["state"] = "normal"

    def Activation_function(self):
        """
        """
        if self.boolead_path.get() == True:
            self.Creation_data()
            
        else:
            print("no se activo ni mierda")

    def Creation_data(self):
        

        try :
            self.diccionario = Diccionario(self.string_path.get())
            Data = Diccionario(self.string_path.get())
            self.combo_cluster1["state"] = "normal"
            self.combo_cluster1["value"] = Data.list_cluster
            self.combo_cluster2["value"] = Data.list_cluster
            self.combo_type_analysis["state"] = "normal"

        except:
            messagebox.showerror(parent = self.master, message = "La ruta seleccionada no contiene un archivo válido", title = "Error en la carga del archivo")

 # C:/Users/tomas/Documents/IB/Tesis/Neuro/Proyectos/Diccionarios_Datos/jp693/Diccionario_0506

    def Validation_path(self):
        val1 = self.combo_type_file.get() in self.combo_type_file["values"] 
        val2 = self.string_path.get() == ""

        if val1 & ~val2:        
            try:
                message = """Ruta = {}
    Tipo de archivo seleccionado = {}
    ¿Es correcto?""".format(self.string_path.get(),self.combo_type_file.get())
                self.boolead_path.set(messagebox.askyesno(parent = self.master, message = message, title = "Validar") )
                self.Activation_function()
            except:
                messagebox.showerror(parent = self.master, message = "A ocurrido un error", title = "Error en la validación")

        elif ~val1 & val2:
             messagebox.showwarning(parent = self.master, message = "No indico la ruta ni tipo de archivo", title = "Cuidado")
        elif val2:
            messagebox.showwarning(parent = self.master, message = "No indico la ruta", title = "Cuidado")
        else:
            messagebox.showwarning(parent = self.master, message = "No selecciono tipo de archivo", title = "Cuidado")



if __name__ == "__main__":
    Top()

