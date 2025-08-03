# Nombre de alumno: Franco Reyes
# Carrera: Ingenieria en Sistemas de Información
# Numero de Legajo: 10911

# servidor_fifo_read_end.py
import os
import time

FIFO_PATH = "/tmp/server_fifo.txt"

# Paso 1: Crear el FIFO si no existe
if not os.path.exists(FIFO_PATH):
    try:
        os.mkfifo(FIFO_PATH)
        print("FIFO creada exitosamente.")
    except Exception as e:
        print("Error al crear FIFO:", e)

print("Servidor iniciado. Esperando mensajes en", FIFO_PATH)

try:
    while True:
        # Paso 2: Abrir FIFO para lectura
        with open(FIFO_PATH, 'r') as fifo:
            print("FIFO abierto. Esperando mensajes...")

            # Paso 3: Leer línea por línea
            for line in fifo:
                print("Servidor recibió:", line.strip())

            # Paso 4: Si llega aquí, se cerró el lado de escritura → EOF
            print("EOF detectado. Reabriendo FIFO...\n")
            time.sleep(1)

except KeyboardInterrupt:
    print("Servidor interrumpido. Cerrando FIFO...")
    os.remove(FIFO_PATH)