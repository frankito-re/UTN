# Nombre alumno: Franco Genaro Reyes
class EtiquetaHTML:
    etiquetas_validas = ['p', 'h1', 'h2', 'div', 'a', 'span', 'strong', 'em']

    def __init__(self, nombre, contenido='', atributos=None):
        if nombre not in EtiquetaHTML.etiquetas_validas:
            self.nombre = 'p'  # etiqueta por defecto
        else:
            self.nombre = nombre

        self.contenido = contenido
        self.atributos = atributos if atributos else {}

    def agregar_atributo(self, clave, valor):
        self.atributos[clave] = valor

    def renderizar(self):
        atributos_str = ''
        for clave in self.atributos:
            atributos_str += f' {clave}={self.atributos[clave]}'

        return f'<{self.nombre}{atributos_str}>{self.contenido}</{self.nombre}>'