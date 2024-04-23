import matplotlib.pyplot as plt

def calcular_posicion_velocidad_aceleracion(a1, a2, a3, t1, t2, tf):
    intervalos_tiempo = [t * (tf / 1000) for t in range(1001)]

    posiciones = []
    velocidades = []
    aceleraciones = []

    for t in intervalos_tiempo:
        if t <= t1:
            a = a1
        elif t <= t2:
            a = a2
        else:
            a = a3
        
        aceleraciones.append(a)
        v = a * t
        velocidades.append(v)
        s = 0.5 * a * t**2
        posiciones.append(s)

    return intervalos_tiempo, posiciones, velocidades, aceleraciones

# Definir los parámetros del movimiento
a1 = 2  # Aceleración para t <= t1
a2 = 1  # Aceleración para t1 < t <= t2
a3 = -0.5  # Aceleración para t2 < t <= tf
t1 = 5  # Tiempo de cambio de a1 a a2
t2 = 10  # Tiempo de cambio de a2 a a3
tf = 15  # Tiempo final

tiempos, posiciones, velocidades, aceleraciones = calcular_posicion_velocidad_aceleracion(a1, a2, a3, t1, t2, tf)

tabla = {'Tiempo (s)': tiempos, 'Posición (m)': posiciones, 'Velocidad (m/s)': velocidades, 'Aceleración (m/s^2)': aceleraciones}

print("Tabla de valores:")
for key, value in tabla.items():
    print(f"{key} : {value}")

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(tiempos, posiciones, label='Posición')
plt.plot(tiempos, velocidades, label='Velocidad')
plt.legend()
plt.xlabel('Tiempo (s)')
plt.ylabel('Magnitud')
plt.title('Posición y Velocidad vs Tiempo')

plt.subplot(2, 1, 2)
plt.plot(tiempos, aceleraciones, label='Aceleración', color='red')
plt.legend()
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s^2)')
plt.title('Aceleración vs Tiempo')

plt.tight_layout()
plt.show()
