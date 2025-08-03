# Nombre de alumno: Franco Reyes
# Carrera: Ingenieria en Sistemas de Información
# Numero de Legajo: 10911

# servidor_fifo_writer_end.py
import os

FIFO_PATH = "/tmp/server_fifo.txt"

# Verificar si el FIFO existe
if not os.path.exists(FIFO_PATH):
    print(f"FIFO no existe en {FIFO_PATH}")
    exit(1)

try:
    # Abrir FIFO para escritura
    with open(FIFO_PATH, 'w') as fifo:
        print("Escribí un mensaje para el servidor. Enter para enviar. Ctrl+C para salir.")
        while True:
            mensaje = input("> ")
            fifo.write(mensaje + "\n")
            fifo.flush()  # Forzamos el envío inmediato

except KeyboardInterrupt:
    print("\nEscritor interrumpido por el usuario.")
except BrokenPipeError:
    print("El servidor no está escuchando (Broken pipe).")