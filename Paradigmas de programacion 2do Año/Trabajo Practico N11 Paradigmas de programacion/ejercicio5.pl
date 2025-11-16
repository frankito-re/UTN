#  --- HECHOS ---
padre(juan_perez, ana_perez).
padre(juan_perez, luis_perez).
madre(maria_gonzalez, ana_perez).
madre(maria_gonzalez, luis_perez).

#  --- REGLAS ---
hijo(H, P) :- padre(P, H).
hijo(H, M) :- madre(M, H).

#  A y B son hermanos si tienen el mismo padre Y la misma madre y no son la misma persona.
hermano(A, B) :-
    padre(P, A), padre(P, B),
    madre(M, A), madre(M, B),
    A \== B. # A no es igual a B