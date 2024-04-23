# Implemente un programa que dadas el modulo del vector ρ y su angulo, devuelva sus componentes y su modulo un vector (bidimensional) devuelva el angulo y el radio.
import math

def calcular_componentes_modulo_angulo(modulo, angulo_grados):
    angulo_rad = math.radians(angulo_grados)

    x_componente = modulo * math.cos(angulo_rad)
    y_componente = modulo * math.sin(angulo_rad)

    modulo_vector = math.sqrt(x_componente**2 + y_componente**2)

    angulo_vector_rad = math.atan2(y_componente, x_componente)

    angulo_vector_grados = math.degrees(angulo_vector_rad)

    return x_componente, y_componente, modulo_vector, angulo_vector_grados

modulo_vector = 5
angulo_vector = 45

x, y, modulo_resultante, angulo_resultante = calcular_componentes_modulo_angulo(modulo_vector, angulo_vector)

print(f"Componente x: {x}")
print(f"Componente y: {y}")
print(f"Módulo del vector resultante: {modulo_resultante}")
print(f"Ángulo del vector resultante: {angulo_resultante} grados")
