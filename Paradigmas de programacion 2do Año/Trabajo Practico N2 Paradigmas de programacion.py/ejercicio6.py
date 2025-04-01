# Nombre alumno: Franco Genaro Reyes

# Computo. Se debera crear una clase llamada Computo, con su constructor por defecto
# sin parametros, que permitira realizar una serie de calculos sobre un numero entero n.
# Debera crear los siguientes metodos:
# a) Un metodo llamado f actorial que permita calcular el factorial de n. Debera testear
# el metodo instanciando la clase como en todos los ejercicios.
# b) Un metodo llamado suma que calcule la suma de los primeros n numeros enteros.
# c) Un metodo llamado es primo que permita testear si el numero es primo o no.
# d) Un metodo tabla multiplicacion que creara y mostrara la tabla de multiplicar de n.
# e) Un metodo lista divisores que obtenga todos los divisores de n y los retorne en un
# arreglo o lista.

class Computo:
    def __init__(self):
        print('El objeto se ha inicializado')
        
    def factorial(self, n):
        resultado = 1
        for i in range(1, n+1):
            resultado *= i
        return resultado
    
    def suma(self, n):
        resultado = 0
        for i in range(1, n+1):
            resultado += i
        return resultado
    
    def es_primo(self, n):
        if n <= 1:
            return f'El numero no es primo'
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return f'El numero no es primo'
        return f'El numero es primo'
    
    def tabla_multiplicacion(self, n):
        tabla = []
        for i in range(1, 11):
            tabla.append(f'{n} x {i} = {n * i}')
        return tabla
    
    def lista_divisores(self, n):
        return [i for i in range(1, n+1) if n % i == 0] # Usamos compresion

computo1 = Computo()
print(computo1.factorial(5))
print(computo1.suma(5))
print(computo1.es_primo(5))
print(computo1.tabla_multiplicacion(5))
print(computo1.lista_divisores(12))

