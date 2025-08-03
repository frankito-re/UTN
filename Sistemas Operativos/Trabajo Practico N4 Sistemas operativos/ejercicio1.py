import sys
import getopt

# Obtener argumentos desde sys.argv (ignorar el primero que es el nombre del script)
argumentos = sys.argv[1:]

opciones, argumentos_adicionales = getopt.getopt(argumentos, 'n:m:o:')

n = None
m = None
operacion = None

for opt, arg in opciones:
    if opt == '-n':
        n = int(arg)
    elif opt == '-m':
        m = int(arg)
    elif opt == '-o':
        operacion = arg

if operacion == '+':
    print('Resultado:', n + m)
elif operacion == '-':
    print('Resultado:', n - m)
elif operacion == '*':
    print('Resultado:', n * m)
elif operacion == '/':
    print('Resultado:', n / m)
else:
    print('Operación no válida')