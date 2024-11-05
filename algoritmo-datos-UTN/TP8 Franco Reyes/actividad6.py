def eliminar_vocales(caracteres):
    vocales = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
    return [c for c in caracteres if c not in vocales]