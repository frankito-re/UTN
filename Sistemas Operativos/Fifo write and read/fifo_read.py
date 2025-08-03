import os

fifo_path = '/Users/d3ksur/Proyectos Mios/Fifo write and read/texto.txt'

os.pipe()
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print('Esperando datos...')
with open(fifo_path, 'r') as fifo:
    while True:
        linea = fifo.readline()
        if linea == '':
            break
        print(f'Recibido: {linea.strip()}')