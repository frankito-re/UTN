import os
import sys
import getopt

argumentos = sys.argv[1:]
opciones, _ = getopt.getopt(argumentos, "n:vh")
numero = None
verbose = False

for opt, arg in opciones:
    if opt == "-n":
        numero = int(arg)
    elif opt == "-v":
        verbose = True
    elif opt == "-h":
        print("Uso: python3 ejercicio4.py -n <cantidad> [-v] [-h]")
        sys.exit()

if numero is None:
    print("Falta el argumento -n")
    sys.exit(1)

for i in range(numero):
    pid = os.fork()
    if pid == 0:
        if verbose:
            print(f"Starting process {os.getpid()}")
        pid_actual = os.getpid()
        ppid = os.getppid()
        suma_pares = sum(num for num in range(0, pid_actual + 1, 2))
        print(f"{pid_actual} - {ppid}: {suma_pares}")
        if verbose:
            print(f"Ending process {os.getpid()}")
        os._exit(0)
    else:
        pass

for _ in range(numero):
    os.wait()