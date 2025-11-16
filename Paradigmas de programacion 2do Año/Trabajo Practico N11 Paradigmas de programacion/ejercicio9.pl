# --- HECHOS ---
encargado_de_tarea(miguel, admision).
encargado_de_tarea(miguel, control).
encargado_de_tarea(miguel, vigilancia).
encargado_de_tarea(ricardo, planificacion).
encargado_de_tarea(ricardo, asesoramiento).
encargado_de_tarea(alicia, direccion).
encargado_de_tarea(alicia, control). # Alicia comparte 'control' con Miguel

ceo(elon).

# --- REGLAS ---
comparten_tarea(P1, P2) :-
    encargado_de_tarea(P1, T),
    encargado_de_tarea(P2, T),
    P1 \== P2.

comparte_y_no_es_ceo(P1, P2) :-
    comparten_tarea(P1, P2),
    \+ ceo(P1),
    \+ ceo(P2).

# 3. Solo Elon es el CEO
# Esto no es una regla, sino una consecuencia del
# único hecho: ceo(elon).
# Cualquier consulta ?- ceo(X) solo dará X = elon.