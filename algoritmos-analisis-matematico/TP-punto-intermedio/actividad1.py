# Calcular sus ceros en el intervalo dado utilizando el teorema de valor intermedio: 𝑓(𝑥)=𝑥2−2𝑥  en [1,5]
def funcion(x):
    return x**2 - 2*x

def encontrar_cero(intervalo, tolerancia):
    a, b = intervalo
    iteraciones = 0
    while abs(b - a) > tolerancia:
        c = (a + b) / 2
        if funcion(c) == 0:
            break
        elif funcion(a) * funcion(c) < 0:
            b = c
        else:
            a = c
        iteraciones += 1
    cero_2_cifras = round(c, 2)
    cero_3_cifras = round(c, 3)
    print(f"Iteraciones necesarias: {iteraciones}")
    print(f"Cero con 2 cifras significativas: {cero_2_cifras}")
    print(f"Cero con 3 cifras significativas: {cero_3_cifras}")
    return c

intervalo = [1, 5]
tolerancia = 0.01
cero = encontrar_cero(intervalo, tolerancia)
