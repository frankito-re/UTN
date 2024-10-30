# Hace un monton de años había una sucursal del correo que tenía un cartel que decía No se
# recibiran mas de 5 cartas por persona. O sea que la gente entregaba sus cartas (hasta la
# cantidad permitida) y luego tenía que volver a hacer la cola si tenía mas cartas para
# despachar.
# Modelar una cola de correo generalizada. La cantidad de cartas que se reciben por persona
# puede usted modificarla a otro valor distinto de 5.d

cola_clientes = [
        ("Juan", 5),
        ("María", 6),
        ("Pedro", 3),
        ("Ana", 2)
    ]

def correo(cartas_permitidas):
    while cola_clientes:
        nombre, numero_cartas = cola_clientes.pop(0)
        
        if numero_cartas > cartas_permitidas:
            print(f"{nombre} despacha {cartas_permitidas} cartas y le quedan {numero_cartas - cartas_permitidas} cartas.")
            cola_clientes.append((nombre, numero_cartas - cartas_permitidas))
        else:
            # Si tiene menos o igual cartas que el límite, despacha todo y sale de la cola
            print(f"{nombre} despacha todas sus {numero_cartas} cartas y se va.")
        
        
correo(5)