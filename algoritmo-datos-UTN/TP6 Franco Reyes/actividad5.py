# 5. Realizar un programa que permita ingresar al usuario todos los vehículos que tienen en su familia.
# a. Crear una clase llamada Vehiculo.
# b. La clase debe contener los atributos: marca, modelo, patente, color.
# Guardar los vehículos en una lista. Finalmente, se deberán mostrar en pantalla todas las marcas de
# vehículos que la familia tiene. Con un conteo de cuántos en total vehículos de cada marca tienen.

class Vehiculo:
    def __init__(self, marca, patente, color):
        self.marca = marca
        self.patente = patente
        self.color = color
        
# Crear una lista de diccionarios con la información de los vehículos
datos_vehiculos = [
    {'marca': 'BMW', 'patente': 'ASD124', 'color': 'Blanco'},
    {'marca': 'Chevrolet', 'patente': 'JMI892', 'color': 'Negro'},
    {'marca': 'Hyundai', 'patente': 'GWA325', 'color': 'Rojo'},
]

# Crear los objetos Vehiculo a partir de los datos
vehiculos_familia = [Vehiculo(**datos) for datos in datos_vehiculos]

# Obtener las marcas de todos los vehículos
marcas = [vehiculo.marca for vehiculo in vehiculos_familia]

print(f'Las marcas que tiene la familia son: {", ".join(marcas)}')
