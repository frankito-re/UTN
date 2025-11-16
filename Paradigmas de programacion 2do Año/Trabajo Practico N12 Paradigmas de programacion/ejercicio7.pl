# Caso base: La longitud de una lista vacía es 0.
longitud_lista([], 0).

# Caso recursivo: Long([_|Cola]) = 1 + Long(Cola)
# (No nos importa el valor de la cabeza, solo que existe)
longitud_lista([_|Xs], L) :-
    longitud_lista(Xs, LCola), # Calcula la longitud del resto
    L is 1 + LCola.           # Suma 1

# Consulta de ejemplo:
# ?- longitud_lista([a, b, c, d], L).
# L = 4.