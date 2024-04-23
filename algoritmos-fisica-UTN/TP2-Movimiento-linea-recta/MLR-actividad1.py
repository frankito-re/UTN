
def calcular_velocidad_altura_gravedad(v0, h0, g, t):
    v = v0 - g * t

    h = h0 + v0 * t - 0.5 * g * t**2

    return v, h

def generar_tabla(v0, h0, g, t_inicial, t_final, paso):
    tabla = []
    tiempo = t_inicial
    while tiempo <= t_final:
        v, h = calcular_velocidad_altura_gravedad(v0, h0, g, tiempo)
        tabla.append((tiempo, v, h))
        tiempo += paso
    return tabla

g = float(input("Ingrese la aceleración de la gravedad (m/s^2): "))
v0 = float(input("Ingrese la velocidad inicial (m/s): "))
h0 = float(input("Ingrese la altura inicial (m): "))
t = float(input("Ingrese el tiempo en el que desea calcular la velocidad y altura (s): "))

velocidad, altura = calcular_velocidad_altura_gravedad(v0, h0, g, t)

print(f"Velocidad en {t} segundos: {velocidad} m/s")
print(f"Altura en {t} segundos: {altura} metros")

opcion = input("¿Desea generar una tabla de tiempo, posición y velocidad? (s/n): ")
if opcion.lower() == 's':
    t_inicial = float(input("Ingrese el tiempo inicial (s): "))
    t_final = float(input("Ingrese el tiempo final (s): "))
    paso = float(input("Ingrese el paso de tiempo (s): "))

    tabla = generar_tabla(v0, h0, g, t_inicial, t_final, paso)
    print("\nTabla de tiempo, posición y velocidad:")
    print("Tiempo (s) | Velocidad (m/s) | Altura (m)")
    for tiempo, velocidad, altura in tabla:
        print(f"{tiempo:.2f} | {velocidad:.2f} | {altura:.2f}")
