# Simulación de una cola de impresión: Crear una función que simule una cola de impresión.
# Los elementos de la cola serán diccionarios con los campos 'documento' y 'paginas'.
cola_impresion = []

def agregar_documento(cola, documento, paginas):
    cola.append({'documento': documento, 'paginas': paginas})
    print(f"Documento '{documento}' con {paginas} páginas añadido a la cola.")



def imprimir_documentos(cola):
    # Procesa la cola de impresión
    while cola:
        documento_actual = cola.pop(0)
        nombre = documento_actual['documento']
        paginas = documento_actual['paginas']
        print(f"Imprimiendo '{nombre}' con {paginas} páginas.")
    
    print("La cola de impresión está vacía.")
        
    
agregar_documento(cola_impresion, "Documento1", 10)
agregar_documento(cola_impresion, "Documento2", 5)
agregar_documento(cola_impresion, "Documento3", 15)
# Procesar la cola de impresión
imprimir_documentos(cola_impresion)