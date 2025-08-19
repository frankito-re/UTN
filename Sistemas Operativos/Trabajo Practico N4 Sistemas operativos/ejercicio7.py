# fin_por_senal_sin_handler.py
import os, time, signal

pid = os.fork()

if pid == 0:
    # ---- HIJO ----
    # Bloquear SIGUSR1 para que quede pendiente cuando llegue
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})
    while True:
        print("Esperando señal...", flush=True)
        time.sleep(3)
        # ¿Llegó la señal? (quedará en pendientes porque está bloqueada)
        if signal.SIGUSR1 in signal.sigpending():
            # (opcional) Desbloquear antes de salir
            signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGUSR1})
            print("Señal recibida, finalizando proceso.", flush=True)
            os._exit(0)
else:
    # ---- PADRE ----
    time.sleep(10)
    os.kill(pid, signal.SIGUSR1)
    os.waitpid(pid, 0)