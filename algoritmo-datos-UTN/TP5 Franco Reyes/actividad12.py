n_5_counter = 0
file_path = '/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP5 Franco Reyes/number5.txt'

with open(file_path, 'r') as number5:
    for number in number5.read():
        if number == '5':
            n_5_counter += 1
            print(n_5_counter)
            
print(f'La cantidad de veces que esta el numero 5 es: {n_5_counter}') 