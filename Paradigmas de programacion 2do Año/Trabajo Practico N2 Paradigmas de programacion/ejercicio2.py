# Nombre alumno: Franco Genaro Reyes
from math import pi

class Circulo:
    def __init__(self, radio):
        self.radio = radio
    
    def calculo_area(self):
        return pi*self.radio**2
    
    def calculo_circunferencia(self):
        return 2*pi*self.radio

circulo1 = Circulo(5)
print(f'El area del circulo1 es {circulo1.calculo_area()} y su circunferencia mide {circulo1.calculo_circunferencia()}')
