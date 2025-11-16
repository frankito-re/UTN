# Caso base: El factorial de 0 es 1.
factorial(0, 1).

# Caso recursivo: N! = N * (N-1)!
factorial(N, F) :-
    N > 0,                # Condición para evitar recursión infinita
    N1 is N - 1,          # Calculamos N-1
    factorial(N1, F1),    # Obtenemos el factorial de N-1
    F is N * F1.          # F es N * (el factorial de N-1)

# Consulta de ejemplo:
# ?- factorial(5, F).
# F = 120.