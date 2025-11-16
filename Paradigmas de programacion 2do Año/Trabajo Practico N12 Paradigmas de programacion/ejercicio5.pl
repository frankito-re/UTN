# --- HECHOS ---
alumno(1001, nombre("Juan", "Perez"), [7, 8, 5, 9]).
alumno(1002, nombre("Ana", "Gomez"), [10, 9, 10, 8]).
alumno(1003, nombre("Luis", "Martinez"), [4, 6, 5, 4]).
alumno(1004, nombre("Maria", "Lopez"), [8, 7, 9, 8]).
alumno(1005, nombre("Carlos", "Sanchez"), [6, 5, 7, 6]).
alumno(1006, nombre("Laura", "Diaz"), [9, 9, 8, 10]).

# --- CONSULTAS ---

# Cómo le fue a un alumno puntual (por nombre), todas sus notas.
# ?- alumno(_, nombre("Ana", "Gomez"), Notas).
# Notas = [10, 9, 10, 8].

# Cómo le fue a otro alumno (por nombre) en el examen 1.
# Se usa "Pattern Matching" en la lista de notas.
# ?- alumno(_, nombre("Luis", "Martinez"), [Nota1, _, _, _]).
# Nota1 = 4.

# Cómo se llama el alumno de un legajo determinado (ej: 1005).
# ?- alumno(1005, NombreCompleto, _).
# NombreCompleto = nombre("Carlos", "Sanchez").