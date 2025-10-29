import mmap
import os
import time

# Creamos un mapa de memoria ANÓNIMO
# -1 indica que no está asociado a ningún archivo
# 1024 es el tamaño
# flags=mmap.MAP_SHARED hace que sea compartido entre procesos
mm = mmap.mmap(-1, 1024, flags=mmap.MAP_SHARED, 
               prot=mmap.PROT_READ | mmap.PROT_WRITE)

# Escribimos datos iniciales
mm.write(b'Datos iniciales del PADRE\x00')

# Creamos un nuevo proceso hijo
pid = os.fork()

if pid == 0:
    # --- Código del PROCESO HIJO ---
    print("[HIJO]: Proceso hijo iniciado.")
    
    # El hijo espera 1 segundo
    time.sleep(1)
    
    # El hijo lee lo que hay en la memoria
    mm.seek(0)
    print(f"[HIJO]: Lei: '{mm.readline().decode('utf-8')}'")
    
    # El hijo escribe en la memoria
    print("[HIJO]: Escribiendo mensaje...")
    mm.seek(0)
    mm.write(b'Mensaje escrito por el HIJO\x00')
    
    print("[HIJO]: Terminando.")
    os._exit(0) # El hijo debe terminar con os._exit()

else:
    # --- Código del PROCESO PADRE ---
    print("[PADRE]: Proceso padre esperando al hijo...")

    # Esperamos a que el hijo lea y escriba
    time.sleep(3) 

    # El padre lee lo que dejó el HIJO
    mm.seek(0)
    print(f"[PADRE]: Lei lo que dejo el hijo: '{mm.readline().decode('utf-8')}'")

    # Esperamos a que el proceso hijo termine completamente
    os.wait() 
    
    print("[PADRE]: Hijo termino. Cerrando mapa.")
    mm.close()