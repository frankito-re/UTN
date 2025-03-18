def max_lista(numeros):
    if len(numeros) == 1:
        return numeros[0]
    else:
        max_del_resto = max_lista(numeros[1:])
        return max(numeros[0], max_del_resto)

nros = [1, 4, 76, 3, 5, 8]
resultado = max_lista(nros)
print(f"El valor máximo de la lista {nros} es: {resultado}")
