def es_consonante(letra):
    vocales = "aeiouAEIOU"  # Lista de vocales
    return letra.isalpha() and letra not in vocales

letra = input("Ingrese una letra: ")
if es_consonante(letra):
    print(f"{letra} es una consonante.")
else:
    print(f"{letra} NO es una consonante.")
