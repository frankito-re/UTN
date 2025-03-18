num = int(input("Ingrese un numero entero: "))

print(f'El numero elevado al cuadrado es: {num**2}\n')
print('\nPrint del metodo locals: ')
print(locals())

# El cambio que hay es solo en las variables declaradas, al final del diccionario dado por el metodo locals()
print('\nPrint del metodo locals con las variables inventadas: ')
var_one = 'Hola! Como estas?'
var_two = 24

print(locals())