# --- HECHOS ---
prestado(
    libro("Misericordia", autor("Benito", "Pérez", "Galdós")),
    persona("Almudena", "Alegría", "Sol")
).
prestado(
    libro("Cien años de soledad", autor("Gabriel", "García", "Márquez")),
    persona("Rodrigo", "Duque", "Soto")
).
prestado(
    libro("El túnel", autor("Ernesto", "Sábato", "")),
    persona("Ana", "Garrido", "Aguirre")
).
prestado(
    libro("Ficciones", autor("Jorge Luis", "Borges", "")),
    persona("Marta", "Cantero", "Lasa")
).
prestado(
    libro("Rayuela", autor("Julio", "Cortázar", "")),
    persona("Rodrigo", "Duque", "Soto")
).

# --- REGLA ---
# Un escritor es leído si alguno de sus libros está prestado.
# La variable 'Autor' es la estructura completa autor(N, A1, A2).
escritor_es_leido(Autor) :-
    prestado(libro(_, Autor), _).

# --- CONSULTAS ---

# Si un lector tiene prestado algún libro (ej: Almudena Alegría Sol)
# ?- prestado(Libro, persona("Almudena", "Alegría", "Sol")).
# Libro = libro("Misericordia", autor("Benito", "Pérez", "Galdós")).

# Si un libro está prestado a alguien (ej: "El túnel")
# ?- prestado(libro("El túnel", _), Quien).
# Quien = persona("Ana", "Garrido", "Aguirre").

# Si una persona es un escritor (ej: "Benito Pérez Galdós")
# (Es escritor si al menos uno de sus libros está en el sistema)
# ?- prestado(libro(_, autor("Benito", "Pérez", "Galdós")), _).
# true.

# Si un escritor es leído (Usando la regla)
# ?- escritor_es_leido(autor("Gabriel", "García", "Márquez")).
# true.
# ?- escritor_es_leido(autor("Miguel", "de", "Cervantes")).
# false.

# Si existen autores leídos
# ?- escritor_es_leido(Quien).
# Quien = autor("Benito", "Pérez", "Galdós") ;
# Quien = autor("Gabriel", "García", "Márquez") ...