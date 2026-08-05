def calcular_descuento(monto):
    # Por reglas de negocio, no se aplica si el monto es menor a 100
    if monto < 100:
        return 0
    return monto*0.1