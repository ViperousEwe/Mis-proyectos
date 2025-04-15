

#Definition to ask the User about the date to the excel#

def inputvalidation(prompt):
    while True:
        try:
            valor = int(input(prompt))
            return valor
        except ValueError:
            print("Valor invalidos")

#Welcome to the user#
title = "Hola soporte, bienvenido al programa generador de excel carga masiva TOBO4."
print("\n" + title + "\n" + "-" * len(title) + "\n")

#Value# next step: el usuario tiene ingresar los datos se van a colocar en el excel a expotar teniendo pendiete que se le debe permitir al usuario poder pegar estos datos.
cp = inputvalidation("Favor pegara aqui el listado de CP a colocar en excel: ")

print(cp)


