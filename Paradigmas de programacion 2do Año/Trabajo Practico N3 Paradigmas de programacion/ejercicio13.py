# Nombre alumno: Franco Genaro Reyes
class MensajeCripto:
    def __init__(self):
        self.alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        self.alfabeto_minuscula = self.alfabeto.lower()

    def encriptar(self, mensaje, desplazamiento):
        resultado = ''
        for caracter in mensaje:
            if caracter in self.alfabeto:
                pos = self.alfabeto.index(caracter)
                nueva_pos = (pos + desplazamiento) % len(self.alfabeto)
                resultado += self.alfabeto[nueva_pos]
            elif caracter in self.alfabeto_minuscula:
                pos = self.alfabeto_minuscula.index(caracter)
                nueva_pos = (pos + desplazamiento) % len(self.alfabeto_minuscula)
                resultado += self.alfabeto_minuscula[nueva_pos]
            else:
                resultado += caracter  # dejar espacios, números o símbolos igual
        return resultado

    def desencriptar(self, mensaje, desplazamiento):
        return self.encriptar(mensaje, -desplazamiento)