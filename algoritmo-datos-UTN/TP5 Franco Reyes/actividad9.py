def leer_archivo_y_mostrar_palabras(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
        
        total_lineas = 0
        for linea in lineas:
            palabra = linea.strip()
            print(palabra)
            total_lineas += 1
        
        print(f"Total de líneas en el archivo: {total_lineas}")
    
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")

leer_archivo_y_mostrar_palabras('/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP5 Franco Reyes/notas.txt')
