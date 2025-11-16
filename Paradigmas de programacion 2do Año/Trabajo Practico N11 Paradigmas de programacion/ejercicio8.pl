# --- HECHOS: Género ---
hombre(antonio).
hombre(juan).
hombre(luis).
hombre(rodrigo).
hombre(ricardo).

mujer(isabel).
mujer(ana).
mujer(marta).
mujer(carmen).
mujer(laura).
mujer(alicia).

# --- HECHOS: Matrimonio ---
matrimonio(antonio, ana).
matrimonio(juan, carmen).
matrimonio(luis, isabel).
matrimonio(rodrigo, laura).

# --- HECHOS: Hijos ---
# Hijos de Antonio y Ana
hijo(juan, antonio).
hijo(juan, ana).
hijo(rodrigo, antonio).
hijo(rodrigo, ana).
hija(marta, antonio).
hija(marta, ana).

# Hija de Luis e Isabel
hija(carmen, luis).
hija(carmen, isabel).

# Hijo de Juan y Carmen
hijo(ricardo, juan).
hijo(ricardo, carmen).

# Hija de Rodrigo e Isabel
# (Nota: El práctico indica Rodrigo e Isabel, aunque Rodrigo
# está casado con Laura[cite: 88]. Modelamos los hechos como están escritos).
hija(alicia, rodrigo).
hija(alicia, isabel).


# --- REGLAS ---

# Regla: Matrimonio reflexivo
son_matrimonio(X, Y) :- matrimonio(X, Y).
son_matrimonio(X, Y) :- matrimonio(Y, X).

# Regla auxiliar: Progenitor (Padre o Madre)
progenitor(P, H) :- hijo(H, P).
progenitor(P, H) :- hija(H, P).

# a) Nietos
nieto(N, A) :- progenitor(A, P), progenitor(P, N).

# b) Abuelos
abuelo(A, N) :- nieto(N, A).
# o: abuelo(A, N) :- progenitor(A, P), progenitor(P, N).

# c) Hermanos (comparten al menos 1 progenitor)
hermano(A, B) :-
    progenitor(P, A),
    progenitor(P, B),
    A \== B.

# Regla auxiliar hermana
hermana(A, B) :- hermano(A, B), mujer(A).

# d) Tíos
# Tío es el hermano del progenitor
tio(T, S) :-
    progenitor(P, S),
    hermano(P, T),
    hombre(T).

# e) Tías
# Tía es la hermana del progenitor
tia(T, S) :-
    progenitor(P, S),
    hermana(P, T),
    mujer(T).

# f) Primos
# Primos son hijos de progenitores que son hermanos
primo(A, B) :-
    progenitor(P1, A),
    progenitor(P2, B),
    hermano(P1, P2),
    A \== B. # Evita que A sea su propio primo

# g) Primas
prima(A, B) :- primo(A, B), mujer(A).

# h) Suegros]
# Suegro es el progenitor de la persona con la que P está casado
suegro(S, P) :-
    son_matrimonio(P, C),
    progenitor(S, C).