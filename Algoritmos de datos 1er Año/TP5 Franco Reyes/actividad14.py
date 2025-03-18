import random

file_path = '/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP5 Franco Reyes/numeros_azar.txt'

def crear_archivo_con_numeros(nombre_archivo):
    with open(file_path, 'w') as archivo:
        numeros = [random.randint(1, 100) for _ in range(250)]
        for numero in numeros:
            archivo.write(f"{numero}\n")
    
    print(f"Archivo '{nombre_archivo}' creado y llenado con 250 números al azar entre 1 y 100.")

crear_archivo_con_numeros('numeros_azar.txt')
