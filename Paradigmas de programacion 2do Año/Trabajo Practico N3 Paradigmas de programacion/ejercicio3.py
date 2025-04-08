# Nombre alumno: Franco Genaro Reyes
class Vehiculo:
    def __init__(self, marca, modelo, anio):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    def __str__(self):
        return f"{self.anio} {self.marca} {self.modelo}"

favoritos = []
odiados = []

print("Ingresá 3 autos favoritos de tu grupo de amigos:")
for i in range(3):
    marca = input(f"Marca del auto favorito {i+1}: ")
    modelo = input(f"Modelo: ")
    anio = input(f"Año: ")
    favoritos.append(Vehiculo(marca, modelo, anio))

print("\nIngresá 3 autos más odiados de tu grupo de amigos:")
for i in range(3):
    marca = input(f"Marca del auto odiado {i+1}: ")
    modelo = input(f"Modelo: ")
    anio = input(f"Año: ")
    odiados.append(Vehiculo(marca, modelo, anio))

print("Autos favoritos:")
for auto in favoritos:
    print(auto)

print("Autos más odiados:")
for auto in odiados:
    print(auto)