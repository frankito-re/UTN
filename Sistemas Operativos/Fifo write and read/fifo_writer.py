import os
import time

fifo_path = '/Users/d3ksur/Proyectos Mios/Fifo write and read/texto.txt'

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, 'w') as fifo:
    for i in range(100):
        mensaje = f'Mensaje {i}'
        print(f'Enviando: {mensaje}')
        fifo.write(mensaje + '\n')
        fifo.flush()
        time.sleep(1)