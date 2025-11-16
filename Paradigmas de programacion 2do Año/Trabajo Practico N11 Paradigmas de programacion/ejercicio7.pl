# --- HECHOS ---
amigo(juan, ana).
amigo(ana, miguel).
amigo(luis, isabel).
amigo(miguel, ana).
amigo(laura, juan).
amigo(isabel, luis).

# --- REGLAS ---
amigos_mutuos(X, Y) :-
    amigo(X, Y),
    amigo(Y, X),
    X @< Y. # Para evitar duplicados (ej: ana-miguel y miguel-ana)

# Regla para amigo no correspondido
amigo_no_correspondido(X, Y) :-
    amigo(X, Y),
    \+ amigo(Y, X). # \+ significa 'not' o 'no es demostrable'

# --- CONSULTAS ---
# ¿Cuáles son los amigos de Juan?
# ?- amigo(juan, Quien).
# Respuesta: Quien = ana.

# ¿Quién es amigo de Ana?
# ?- amigo(Quien, ana).
# Respuestas: Quien = juan; Quien = miguel.

# ¿Quién es amigo de quién?
# ?- amigo(X, Y).
# Respuestas: X = juan, Y = ana; X = ana, Y = miguel; ...

# ¿Quiénes son amigos mutuos?
# ?- amigos_mutuos(A, B).
# Respuestas: A = ana, B = miguel; A = isabel, B = luis.

# ¿Quién es amigo sin ser correspondido?
# ?- amigo_no_correspondido(A, B).
# Respuestas: A = juan, B = ana; A = laura, B = juan.