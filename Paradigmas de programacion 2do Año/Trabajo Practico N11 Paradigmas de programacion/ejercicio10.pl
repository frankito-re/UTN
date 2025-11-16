# --- HECHOS ---
juega(hector, baloncesto).
juega(miguel, balonmano).
juega(miguel, rugby).
juega(alicia, tenis).
juega(alicia, baloncesto).
juega(alicia, ajedrez).

# --- REGLAS ---
mismo_deporte(P1, P2) :-
    juega(P1, D),
    juega(P2, D),
    P1 \== P2.

# --- CONSULTAS ---
# ¿Quiénes juegan al ajedrez?
# ?- juega(Quien, ajedrez).
# Respuesta: Quien = alicia.

# ¿Quiénes juegan al mismo deporte?
# ?- mismo_deporte(A, B).
# Respuesta: A = hector, B = alicia (y A = alicia, B = hector)