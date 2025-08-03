import sys
import getopt

argumentos = sys.argv[1:]

opciones, argumentos_adicionales = getopt.getopt(argumentos, 'i:o:')

archivo_entrada = None
archivo_copia = None

print(opciones)

for opt, arg in opciones:
    if opt == '-i':
        archivo_entrada = arg
    elif opt == '-o':
        archivo_copia = arg


if archivo_entrada and archivo_copia:
    try:
        with open(archivo_entrada, 'r') as entrada:
            contenido = entrada.read()
        with open(archivo_copia, 'w') as salida:
            salida.write(contenido)
        print("Archivo copiado correctamente.")
    except FileNotFoundError:
        print("El archivo de entrada no existe.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
else:
    print("Faltan argumentos. Uso: -i archivo_entrada -o archivo_salida")
        
