def division():
    try:
        numerador = float(input("Ingrese el numerador: "))
        divisor = float(input("Ingrese el divisor: "))

        if divisor == 0:
            raise ZeroDivisionError("Error: El divisor no puede ser cero.")

        resultado = numerador / divisor
        print(f"El resultado de la división es: {resultado}")

    except ValueError:
        print("Error: Ingrese solo números.")
    except ZeroDivisionError as error:
        print(error)

division()
