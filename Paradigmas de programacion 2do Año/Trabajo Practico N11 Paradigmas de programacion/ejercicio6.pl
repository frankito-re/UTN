#  --- HECHOS ---
pareja(bruce_wayne, talia_al_ghul).

#  Padres biológicos
padre(bruce_wayne, damian_wayne).
madre(talia_al_ghul, damian_wayne).

#  Primos
primos(bruce_wayne, kate_kane).

#  Hijos adoptivos
adopta(bruce_wayne, dick_grayson).
adopta(bruce_wayne, jason_todd).
adopta(bruce_wayne, tim_drake).
adopta(bruce_wayne, cassandra_cain).

#  --- REGLAS ---
hijo(H, P) :- padre(P, H).
hijo(H, M) :- madre(M, H).

hijo_adoptivo(H, P) :- adopta(P, H).

esposa(E, H) :- pareja(H, E).
esposa(E, H) :- pareja(E, H).

#  --- CONSULTAS ---
#  a) ¿Damian es hijo de Bruce?
#  ?- hijo(damian_wayne, bruce_wayne).
#  Respuesta: true.

#  b) ¿Kate es esposa de Bruce?
#  ?- esposa(kate_kane, bruce_wayne).
#  Respuesta: false.

#  c) ¿Quién es la esposa de Bruce?
#  ?- esposa(Quien, bruce_wayne).
#  Respuesta: Quien = talia_al_ghul.

#  d) ¿Bruce tiene primos?
#  ?- primos(bruce_wayne, Quien).
#  Respuesta: Quien = kate_kane.

#  e) ¿Bruce adoptó hijos?
#  ?- adopta(bruce_wayne, Quien).
#  Respuestas: Quien = dick_grayson; Quien = jason_todd; ...

#  f) ¿Damian es hijo de quién?
#  ?- hijo(damian_wayne, Quien).
#  Respuestas: Quien = bruce_wayne; Quien = talia_al_ghul.