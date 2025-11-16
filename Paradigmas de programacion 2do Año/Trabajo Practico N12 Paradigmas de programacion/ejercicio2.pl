# Caso base 0: fib(0) = 0
fibonacci(0, 0).
# Caso base 1: fib(1) = 1
fibonacci(1, 1).

# Caso recursivo: fib(N) = fib(N-1) + fib(N-2)
fibonacci(N, F) :-
    N > 1,
    N1 is N - 1,
    N2 is N - 2,
    fibonacci(N1, F1),
    fibonacci(N2, F2),
    F is F1 + F2.

# Consulta de ejemplo:
# ?- fibonacci(7, F).
# F = 13.