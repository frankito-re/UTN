# Implemente un programa que pida dos vectores A~ y B~ (las componente x, y de cada uno) y un escalar k y devuelve el vector C~ = k · A~ + B~ (es decir sus 2 componentes) ademas, su modulo y su angulo.

import math

def sumar_vectores_escalar(A, B, k):
    C_x = k * A[0] + B[0]
    C_y = k * A[1] + B[1]
    
    modulo_C = math.sqrt(C_x**2 + C_y**2)

    angulo_C_rad = math.atan2(C_y, C_x)

    angulo_C_grados = math.degrees(angulo_C_rad)

    return C_x, C_y, modulo_C, angulo_C_grados

A_x = float(input("Ingrese la componente x del vector A: "))
A_y = float(input("Ingrese la componente y del vector A: "))
B_x = float(input("Ingrese la componente x del vector B: "))
B_y = float(input("Ingrese la componente y del vector B: "))
k = float(input("Ingrese el escalar k: "))

A = (A_x, A_y)
B = (B_x, B_y)

C_x, C_y, modulo_C, angulo_C = sumar_vectores_escalar(A, B, k)

print(f"El vector C = k * A + B es ({C_x}, {C_y})")
print(f"Su módulo es {modulo_C}")
print(f"Su ángulo es {angulo_C} grados")
