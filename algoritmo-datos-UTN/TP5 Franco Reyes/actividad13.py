file_path = '/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP5 Franco Reyes/number5.txt'

with open(file_path, 'r') as file:
    content = file.read().strip()
    
    numbers = content.split()
    int_numbers = [int(digit) for digit in content if digit.isdigit()]
    
    number_sum = sum(int_numbers)
    average = number_sum / len(content)
    
    print(f'La suma de los numeros es: {number_sum} y el promedio es {average}')