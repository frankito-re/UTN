import os, signal, time, os

N = 10  # cantidad de "ping/pong"

def hijo1():
    ppid = os.getppid()
    for _ in range(N):
        print(f"Hijo1 (PID={os.getpid()}): ping", flush=True)
        os.kill(ppid, signal.SIGUSR1)     # envía al padre
        time.sleep(5)
    os._exit(0)

def hijo2():
    # Bloquea SIGUSR1 y luego espera con sigwait
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})
    for _ in range(N):
        signal.sigwait({signal.SIGUSR1})  # llega desde el padre
        print(f"Hijo2 (PID={os.getpid()}): pong", flush=True)
    os._exit(0)

if __name__ == "__main__":
    # --- crear hijo1 ---
    pid_h1 = os.fork()
    if pid_h1 == 0:
        hijo1()

    # --- crear hijo2 ---
    pid_h2 = os.fork()
    if pid_h2 == 0:
        hijo2()

    # --- PADRE ---
    # El padre también espera señales sin handler
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})

    for _ in range(N):
        signal.sigwait({signal.SIGUSR1})      # llegó desde hijo1
        os.kill(pid_h2, signal.SIGUSR1)       # reenvía a hijo2

    # Cierre limpio (por si alguno quedó esperando)
    try:
        os.kill(pid_h1, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        os.kill(pid_h2, signal.SIGTERM)
    except ProcessLookupError:
        pass

    # Esperar a los hijos
    for pid in (pid_h1, pid_h2):
        try:
            os.waitpid(pid, 0)
        except ChildProcessError:
            pass