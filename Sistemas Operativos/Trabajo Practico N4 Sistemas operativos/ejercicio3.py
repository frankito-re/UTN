import os
import sys
import getopt

numero = int(sys.argv[2])

for i in range(numero):
    pid = os.fork()
    if pid == 0:
        # Código del hijo
        pid_actual = os.getpid()
        ppid = os.getppid()
        suma_pares = sum(num for num in range(0, pid_actual + 1, 2))
        print(f"{pid_actual} - {ppid}: {suma_pares}")
        os._exit(0)  # el hijo termina aquí
    else:
        pass

for _ in range(numero):
    os.wait()