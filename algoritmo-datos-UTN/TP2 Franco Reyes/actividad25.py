numbers_len = []

quantity_number = int(input('Ingrese la cantidad de numeros que quiere analizar: '))

while len(numbers_len) < quantity_number:
    number = input('Ingrese un numero: ')
    numbers_len.append(len(number))
    
print(numbers_len)
    