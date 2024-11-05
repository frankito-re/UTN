# Paso 1: Pedir los límites del intervalo [a, b]
a = int(input("Introduce el límite inferior (a): "))
b = int(input("Introduce el límite superior (b), debe ser mayor que a: "))
# Verificamos que a < b
if a >= b:
    print("El límite superior debe ser mayor que el límite inferior.")
else:
    print(f"Piensa en un número en el intervalo [{a}, {b}] y no lo digas.")
    # Paso 2: Iniciar el proceso de adivinación usando búsqueda binaria
    intentos = 0
    while a <= b:
        # Paso 3: Computadora adivina el número medio
        intento = (a + b) // 2
        intentos += 1
        print(f"¿Es el número {intento}? (Responde con 'mayor', 'menor', 'igual' o 'salir')")
        # Paso 4: Recibir la respuesta del usuario
        respuesta = input().lower()
        # Paso 5: Evaluar la respuesta
        if respuesta == 'igual':
            print(f"¡Adiviné tu número {intento} en {intentos} intentos!")
            break
        elif respuesta == 'mayor':
            a = intento + 1  # El número está en el rango superior
        elif respuesta == 'menor':
            b = intento - 1  # El número está en el rango inferior
        elif respuesta == 'salir':
            print("Has decidido salir del juego. ¡Hasta la próxima!")
            break
        else:
            print("Respuesta no válida. Por favor, responde con 'mayor', 'menor', 'igual' o 'salir'.")
    # Caso en el que los límites se cruzan sin haber adivinado
    if a > b:
        print("Parece que algo salió mal o el número no estaba en el intervalo.")
