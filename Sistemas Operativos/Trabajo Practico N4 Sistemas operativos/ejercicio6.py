# multihijos_simple.py
import os, sys, signal

# Cantidad de hijos: primer argumento o 2 por defecto
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2

# Bloquear SIGUSR2 antes del fork (los hijos heredan esta máscara)
signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR2})

hijos = []
for _ in range(N):
    pid = os.fork()
    if pid == 0:
        # Hijo: esperar la señal y luego imprimir
        signo = signal.sigwait({signal.SIGUSR2})
        print(f"Soy el PID {os.getpid()}, recibí la señal {signo} de mi padre PID {os.getppid()}", flush=True)
        os._exit(0)
    else:
        # Padre: guardar PID del hijo
        hijos.append(pid)
        print(f"Creando proceso: {pid}", flush=True)

# Padre: enviar SIGUSR2 a cada hijo y esperar
for pid in hijos:
    os.kill(pid, signal.SIGUSR2)

for pid in hijos:
    os.waitpid(pid, 0)