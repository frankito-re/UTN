#!/usr/bin/env python3
# TP6 - multiprocessing.Queue: Productor/Consumidor
# Run: python3 queue_python.py

from multiprocessing import Process, Queue
import time

def productor(q: Queue):
    for i in range(1, 6):
        msg = f"Mensaje {i}"
        q.put(msg)           # bloquea si está llena (si tuviera maxsize)
        print(f"[PROD] Enviado: {msg}")
        time.sleep(0.15)

def consumidor(q: Queue):
    for _ in range(5):
        msg = q.get()        # bloquea hasta que haya mensaje
        print(f"[CONS] Recibido: {msg}")

if __name__ == "__main__":
    q = Queue()              # procesos relacionados comparten este handle
    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))
    p1.start(); p2.start()
    p1.join(); p2.join()
    print("Fin.")
