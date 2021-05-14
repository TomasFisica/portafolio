#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO


def Acceso(id, num_adultos, num_niños, cod_mesa, nick, dic_ses, dic_mesa):
    
    if dic_mesa[cod_mesa] != True:
        dic_ses["id"].append(id)
        dic_ses["num_adultos"].append(num_adultos)
        dic_ses["num_niños"].append(num_niños)
        dic_ses["cod_mesa"].append(cod_mesa)
        dic_ses["nick"].append(nick)
        dic_mesa[cod_mesa] = True
        print("Ses", dic_ses)
        print("Mes", dic_mesa)
        return True
    else:
        print("La mesa ya se encuentra ocupada")
        return False

def get_user(nick, cod_mesa, users):
    for user in users:
        if (str(user.nick) == str(nick) )and(str(user.cod_mesa) == str(cod_mesa)):
            return user
    return None