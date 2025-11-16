# ?- N is 4+5. 
# Respuesta: N = 9.
# Por qué: is evalúa la expresión aritmética de la derecha y unifica el resultado con la variable de la izquierda.
# ?- 4+1 =:= 5. 
# Respuesta: true.
# Por qué: =:= evalúa aritméticamente ambos lados y compara los valores numéricos.
# ?- 4+1 == 5. 
# Respuesta: false.
# Por qué: == es la "igualdad de términos" estricta. Comprueba si los términos son idénticos. El término 4+1 (que es +(4, 1)) no es idéntico al término 5.
# ?- 5 == 5. 
# Respuesta: true.
# Por qué: El término 5 es idéntico al término 5.