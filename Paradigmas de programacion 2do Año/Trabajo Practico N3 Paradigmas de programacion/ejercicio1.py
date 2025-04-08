# Nombre alumno: Franco Genaro Reyes
class Perro:
    def __init__(self, nombre, edad, raza):
        self.edad = edad
        self.raza = raza
        self.nombre = nombre  

lista_perros = []
edad_mayor = 0

for i in range(6):
    nombre = input(f'Ingresá el nombre del perro {i+1}: ')
    edad = int(input(f'Ingresá la edad de {nombre}: '))
    raza = str(input(f'Ingresá la raza de {nombre}: '))
    perro = Perro(nombre, edad, raza)
    lista_perros.append(perro)
    
edad_mayor = lista_perros[0].edad

for i in range(1, len(lista_perros)):
    if lista_perros[i].edad > edad_mayor:
        edad_mayor = lista_perros[i].edad

print(edad_mayor)