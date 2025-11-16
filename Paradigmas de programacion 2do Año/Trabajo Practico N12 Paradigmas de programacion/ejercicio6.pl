# Caso base: La suma de una lista vacía es 0.
sumar_lista([], 0).

# Caso recursivo: Suma([Cabeza|Cola]) = Cabeza + Suma(Cola)
sumar_lista([X|Xs], Suma) :-
    sumar_lista(Xs, SumaCola), # Suma el resto de la lista
    Suma is X + SumaCola.      # Suma la cabeza al resultado

# Consulta de ejemplo:
# ?- sumar_lista([5, 10, 3], S).
# S = 18.