# Pedir numeros al usuario y almacenarlos en una lista, hasta que el usuario ingrese la
# letra q para salir

condition_while = True
n_list = []

while condition_while:
    n = input('Ingresa algún numero o la letra "q" para salir: ')
    if n == 'q':
        condition_while = False
    else:
        n_list.append(n)
    
print(n_list)