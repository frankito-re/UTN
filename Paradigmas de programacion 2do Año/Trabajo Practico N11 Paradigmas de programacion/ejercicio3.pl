# 3a) Colores de frutas
color(naranja, naranja).
color(pomelo, amarillo).
color(frutilla, rojo).
color(avocado, verde).  'avocado' es palta

# 3b) Animales y amigos
perro(sultan).
perro(fideo).
perro(dago).
gato(mimu).
gato(kitty).
gato(ona).

amigos(ona, fideo).
amigos(fideo, sultan).
amigos(kitty, ona).

# 3c) Frutas comibles
fruta(manzana).
fruta(naranja).
 Regla: Algo es comible si es una fruta
es_comible(X) :- fruta(X).

# 3d) Lucia en el bar
esta_en_bar(lucia).
esta_en_bar(frodo).
esta_contenta(lucia).

# Regla: Lucia canta si está en un bar Y contenta
canta(lucia) :- esta_en_bar(lucia), esta_contenta(lucia).

# Consulta: ¿Lucia está cantando?
# ?- canta(lucia).
# Respuesta: true.