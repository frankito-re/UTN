# Dado un archivo de texto con algunas líneas de texto dentro, cualesquiera, realizar un
# programa que genere un archivo de texto llamado invertido.txt que contenga las líneas en
# orden inverso al archivo de texto original.

with open("/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP7 Franco Reyes/actividad7.txt", "r") as file:
    lineas = file.readlines()
with open("/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP7 Franco Reyes/invertido.txt", "w") as file_invertido:
    
    while lineas:
        element = lineas.pop()
        file_invertido.write(element)