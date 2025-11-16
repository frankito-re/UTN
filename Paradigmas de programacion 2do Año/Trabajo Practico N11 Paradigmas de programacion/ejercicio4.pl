# color(zanahoria, naranja).  -> "La zanahoria es de color naranja".
# padre(pablo, juan).  -> "Pablo es el padre de Juan".
# madre(maria, ana).  -> "María es la madre de Ana".
# gusta(Persona, zanahoria) :- vegetariana(Persona).  -> "A una 'Persona' le gusta la zanahoria SI la 'Persona' es vegetariana".
# aprueba(Estudiante) :- estudia_mucho(Estudiante).  -> "Un 'Estudiante' aprueba SI 'estudia mucho'".
# ?- aprueba(Quien).  -> Consulta: "¿Quién aprueba?" (Busca un valor para 'Quien' que haga la regla aprueba verdadera).
# ?- dicta(profesor, Curso).  -> Consulta: "¿Qué 'Curso' dicta el 'profesor'?"
# enemigos(X, Y) :- odia(X, Y), pelea(X, Y).  -> "'X' e 'Y' son enemigos SI 'X' odia a 'Y' Y 'X' pelea con 'Y'".