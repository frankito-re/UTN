# Nombre alumno: Franco Genaro Reyes
from datetime import datetime
def funcion_escritura(funcion_original):
    def wrapper():
        hora_formateada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/Users/d3ksur/Proyectos Mios/UTN/Paradigmas de programacion 2do Año/Trabajo Practico N4 Paradigmas de programacion/archivo.txt', 'w') as file:
            file.write(f'Fecha y hora de llamada: {hora_formateada}\n')
            file.write(f'El nombre de la funcion llamada es: {funcion_original.__name__}')
        funcion_original()
    return wrapper

@funcion_escritura
def funcion_a_decorar():
    pass

funcion_a_decorar()