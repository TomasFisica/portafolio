#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO


def Generador_Dicc(Datos_brutos):
    """Funcion que genera los diccionarios a utilizar. Dicha funcion recibe como entrada a los nombres de los experimentos"""
    
    
    for k in Datos_brutos:
        datos={}
        Nombre_animales="/home/tomasg/Escritorio/Neuro/data_perez_escobar_2016/circular_arena/{}" #Debo indicar el nombre del animal
        
        
        List_ses=listdir(Nombre_animales.format(k))
        Sessiones=[]    #Creo la lista de sessiones
        for i in List_ses:
            Ses=i[i.find("-")+1:i.find("2015")]
            Sessiones.append(Ses)
        Nombre2="/home/tomasg/Escritorio/Neuro/data_perez_escobar_2016/circular_arena/{}/{}-{}2015-0108/{}-{}2015-0108.{}"
        Nombre1="{}-{}2015-0108".format(k,"{}") 
        Nombre_clu=Nombre2.format(k,k,"{}",k,"{}","clu")
        Nombre_res=Nombre2.format(k,k,"{}",k,"{}","res")
        Nombre_light=Nombre2.format(k,k,"{}",k,"{}","light_trials_intervals")
        Nombre_whl=Nombre2.format(k,k,"{}",k,"{}","whl")
        #En el siguiente apartado cargo los datos principales para refinar los datos
        for i in Sessiones:
            datos[Nombre1.format(i)]={"Clu":np.loadtxt(Nombre_clu.format(i,i)),"Res":np.loadtxt(Nombre_res.format(i,i)),"Light":np.loadtxt(Nombre_light.format(i,i),dtype=str)}
        
        """Cargo los archivos"""
        
        #Abajo indico la ruta y el nombre con el que se guardaran los archivos
        Nombre_Guardar="/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu/Diccionarios_Datos/{}/Diccionario_{}" 
        """Refino y guardo los datos"""
        
        Dic={}
        for l in Sessiones:
            Dic=Division_global(datos[Nombre1.format(l)]["Clu"], datos[Nombre1.format(l)]["Res"], datos[Nombre1.format(l)]["Light"])
            Dic["Posicion"]=np.loadtxt(Nombre_whl.format(l))    #Agrego al diccionario los datos de la posicion
            Dic["Light_Trials"]=datos[Nombre1.format(l,l)]["Light"]  #Agrego al diccionario los datos de intervalos de luz y oscuridad utilizados
            Guardar(Nombre_Guardar.format(k,l),Dic) # l es la session donde se guarda y k el codigo del animal


from os import listdir
listdir("/home/tomasg/Escritorio/Neuro/Lectura de Datos/Generacion de Dicc_Clu")



List_ses=listdir("/home/tomasg/Escritorio/Neuro/data_perez_escobar_2016/circular_arena/jp693")
Sessiones=[]
for i in Num_ses:
    Ses=i[i.find("-")+1:i.find("2015")]
    Sessiones.append(Ses)