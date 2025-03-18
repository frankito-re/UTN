def contar_apariciones(s, a):
    contador = 0
    actual = s
    # Recorremos la lista mientras haya nodos
    while actual is not None:
        if actual.dato == a:
            contador += 1
        actual = actual.siguiente
    return contador