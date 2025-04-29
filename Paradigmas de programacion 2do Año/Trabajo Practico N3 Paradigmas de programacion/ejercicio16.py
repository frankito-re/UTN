# Nombre alumno: Franco Genaro Reyes
class Vehiculo:
    def __init__(self, marca, modelo, anio):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    def __str__(self):
        return f"{self.anio} {self.marca} {self.modelo}"

class AutoParticular(Vehiculo):
    def __init__(self, marca, modelo, anio, estado, precio):
        super().__init__(marca, modelo, anio)
        self.estado = estado
        self.precio = precio

class Camioneta(Vehiculo):
    def __init__(self, marca, modelo, anio, es4x4):
        super().__init__(marca, modelo, anio)
        self.es4x4 = es4x4

class Moto(Vehiculo):
    def __init__(self, marca, modelo, anio, color):
        super().__init__(marca, modelo, anio)
        self.color = color

class Omnibus(Vehiculo):
    def __init__(self, marca, modelo, anio, asientos):
        super().__init__(marca, modelo, anio)
        self.asientos = asientos

auto_particular1 = AutoParticular('Volkswagen', 'Amarok', 2019, 'Nuevo', 25000000)
camioneta1 = Camioneta('Toyota', 'Hilux', 2021, True)
moto1 = Moto('Yamaha', 'FZ', 2020, 'Rojo')
omnibus1 = Omnibus('Mercedes-Benz', 'Sprinter', 2018, 24)

print(auto_particular1)
print(camioneta1)
print(moto1)
print(omnibus1)

#           Vehiculo
#       /   |       |    \
#Auto P.  Camioneta Moto  Omnibus