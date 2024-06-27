with open('/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP5 Franco Reyes/file.txt', 'w') as file:
    for number in range(1, 11):
        file.write(f'{number}')
    print("Se han agregado números al archivo.")