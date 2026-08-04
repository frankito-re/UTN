def validar_contrasenia(password: str):
    tiene_numero = any(caracter.isdigit() for caracter in password)
    return len(password) >= 8 and tiene_numero