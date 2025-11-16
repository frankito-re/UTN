# ?- animal(perro).  -> true. (Es un hecho definido en la base).
# ?- animal(pelicula).  -> false. (No existe el hecho animal(pelicula)).
# ?- espajaro(gato).  -> false. (No existe el predicado espajaro/1. Si la consulta fuera es_ave(gato), también sería false).
# ?- es_ave(perro).  -> false. (El hecho es es_mamifero(perro)).