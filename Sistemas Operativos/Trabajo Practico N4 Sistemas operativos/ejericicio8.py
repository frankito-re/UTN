import os, sys, time, random

if len(sys.argv) != 3 or sys.argv[1] != "-n":
    print(f"Uso: {sys.argv[0]} -n <cantidad>")
    sys.exit(1)

try:
    n = int(sys.argv[2])
except ValueError:
    print("Cantidad debe ser un número entero")
    sys.exit(1)

# Crear n hijos
for _ in range(n):
    pid = os.fork()
    if pid == 0:
        # ---- HIJO ----
        tiempo = random.randint(1, 5)
        time.sleep(tiempo)
        print(f"Soy el hijo PID {os.getpid()} y terminé luego de {tiempo} segundos", flush=True)
        os._exit(0)

# ---- PADRE ----
for _ in range(n):
    os.wait()   # esperar a cada hijo