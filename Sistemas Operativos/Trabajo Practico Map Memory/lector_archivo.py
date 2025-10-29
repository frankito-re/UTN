import mmap
import os
import time

# Nombre del archivo que compartimos (DEBE SER EL MISMO)
archivo_mapa = 'memoria.dat'

# Esperamos un segundo a que el escritor cree el archivo
time.sleep(1)

# Abrimos el archivo existente en modo "r+b" (lectura/escritura binaria)
try:
    f = open(archivo_mapa, 'r+b')
except FileNotFoundError:
    print("Error: El archivo 'memoria.dat' no existe. Ejecuta el escritor primero.")
    exit()

# Creamos el mapa de memoria
mm = mmap.mmap(f.fileno(), 1024)

# Leemos lo que escribió el escritor
mm.seek(0)  # Vamos al inicio
mensaje_leido = mm.read(100).strip(b'\x00') # Leemos 100 bytes y quitamos ceros

print(f"LECTOR: Lei: '{mensaje_leido.decode('utf-8')}'")

# Ahora escribimos una respuesta
print("LECTOR: Escribiendo respuesta...")
mm.seek(0) # Sobreescribimos el inicio
mm.write(b'Respuesta del LECTOR! Adios!\x00')
mm.flush()

# Cerramos todo
mm.close()
f.close()