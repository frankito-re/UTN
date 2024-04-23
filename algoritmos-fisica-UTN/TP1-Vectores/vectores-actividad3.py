# Implemente un programa que dadas las componentes x e y de un vector (bidimensional) devuelva el angulo, el radio y su modulo.
import math

def calcular_angulo_radio_modulo(x, y):
    angulo_rad = math.atan2(y, x)
    
    angulo_grados = math.degrees(angulo_rad)

    radio = math.sqrt(x**2 + y**2)

    modulo = abs(radio)

    return angulo_grados, radio, modulo

x_componente = 3
y_componente = 4
angulo, radio, modulo = calcular_angulo_radio_modulo(x_componente, y_componente)

print(f"Ángulo: {angulo} grados")
print(f"Radio: {radio}")
print(f"Módulo: {modulo}")
