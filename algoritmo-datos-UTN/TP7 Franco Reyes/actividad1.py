# Diseñar un algoritmo que a partir de una pila inicial de tres elementos devuelva una pila
# invertida de dichos elementos. La pila inicial se encuentra vacía, usted deberá´ apilar los
# elementos y mostrar la pila original. Luego invertir los elementos, y mostrar la nueva pila
# invertida.

# Metodo de slicing
pila = [3, 2, 1]
pila_invertida = pila[::-1]

print(pila_invertida)

# Metodo reverse
pila_reverse = [3, 2, 1]
pila_reverse.reverse()

print(pila)
