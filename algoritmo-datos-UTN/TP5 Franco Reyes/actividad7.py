def paridad_lista(numeros):
    if not numeros:
        return []
    else:
        es_par = numeros[0] % 2 == 0
        return [es_par] + paridad_lista(numeros[1:])
    
nros = [1, 4, 76, 3, 5, 8]
resultado = paridad_lista(nros)
print(f"nros = {nros}")
print(f"resultado = {resultado}")
