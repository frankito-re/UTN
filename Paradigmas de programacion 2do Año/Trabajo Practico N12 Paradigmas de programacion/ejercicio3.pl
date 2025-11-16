# --- HECHOS ---
# (Se inventan 7 lectores más para llegar a 10)
lector(nombre("Ana", "Garrido", "Aguirre"), mujer, 31).
lector(nombre("Marta", "Cantero", "Lasa"), mujer, 20).
lector(nombre("Rodrigo", "Duque", "Soto"), hombre, 30).
lector(nombre("Carlos", "Gomez", "Paz"), hombre, 45).
lector(nombre("Lucia", "Perez", "Mar"), mujer, 28).
lector(nombre("Javier", "Fernandez", "Luna"), hombre, 50).
lector(nombre("Sofia", "Morales", "Rios"), mujer, 19).
lector(nombre("Diego", "Blanco", "Sol"), hombre, 33).
lector(nombre("Elena", "Ruiz", "Cruz"), mujer, 62).
lector(nombre("Rodrigo", "Vega", "Canto"), hombre, 25). # Otro Rodrigo

# --- CONSULTAS ---

# ¿Hay lectores? (Si devuelve 'true' o un resultado, hay)
# ?- lector(_, _, _).

# ¿Quiénes son lectores? (Devuelve los nombres)
# ?- lector(Nombre, _, _).
# Nombre = nombre("Ana", "Garrido", "Aguirre") ;
# Nombre = nombre("Marta", "Cantero", "Lasa") ...

# ¿Qué lectores son mujeres?
# ?- lector(Nombre, mujer, _).
# Nombre = nombre("Ana", "Garrido", "Aguirre") ;
# Nombre = nombre("Marta", "Cantero", "Lasa") ...

# ¿Qué lectores son hombres?
# ?- lector(Nombre, hombre, _).
# Nombre = nombre("Rodrigo", "Duque", "Soto") ;
# Nombre = nombre("Carlos", "Gomez", "Paz") ...

# ¿Hay lectores con el mismo nombre y diferentes apellidos?
# Se buscan dos lectores L1 y L2, con el mismo primer nombre N,
# pero cuyos apellidos (A1,A2) no sean idénticos a (A3,A4).
# Usamos @< para evitar duplicados (ej: A-B y B-A).
# ?- lector(nombre(N, A1, A2), _, _),
#    lector(nombre(N, A3, A4), _, _),
#    (A1 \== A3 ; A2 \== A4),
#    nombre(N, A1, A2) @< nombre(N, A3, A4).
#
# N = "Rodrigo",
# A1 = "Duque", A2 = "Soto",
# A3 = "Vega", A4 = "Canto".