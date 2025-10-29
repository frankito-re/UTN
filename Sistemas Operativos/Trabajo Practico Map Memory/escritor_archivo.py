import mmap
import os
import time

# Nombre del archivo que usaremos como memoria compartida
archivo_mapa = 'memoria.dat'

# Abrimos el archivo en modo "w+b" (escritura/lectura binaria, lo crea si no existe)
# Es importante darle un tamaño inicial
f = open(archivo_mapa, 'w+b')
f.write(b'\x00' * 1024)  # 1KB de espacio inicial (lleno de ceros)
f.close()

# Ahora lo abrimos para mapeo (lectura/escritura)
f = open(archivo_mapa, 'r+b')

# Creamos el mapa de memoria
# El primer argumento es el descriptor del archivo (f.fileno())
# El segundo es el tamaño (1024 bytes)
mm = mmap.mmap(f.fileno(), 1024)

# Escribimos en el mapa de memoria
mm.seek(0)  # Vamos al inicio del mapa
mensaje = b'Hola desde el proceso ESCRITOR!'
mm.write(mensaje)
mm.flush()  # Aseguramos que se escriba en el archivo

print(f"ESCRITOR: Escribi '{mensaje.decode('utf-8')}'")
print("ESCRITOR: Esperando 10 segundos para que el lector lea...")

time.sleep(10)

# El lector puede escribir de vuelta. Leemos lo que dejó.
mm.seek(0)
respuesta = mm.read(100).strip(b'\x00')
print(f"ESCRITOR: Lei de vuelta: '{respuesta.decode('utf-8')}'")

# Cerramos todo
mm.close()
f.close()

# Opcional: eliminar el archivo al final
# os.remove(archivo_mapa)