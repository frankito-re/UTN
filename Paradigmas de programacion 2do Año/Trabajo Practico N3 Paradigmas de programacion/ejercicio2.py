# Nombre alumno: Franco Genaro Reyes
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def modulo(self):
        return (self.x**2 + self.y**2)**1/2
    
    def sumar_vector(self, vector2):
        return Vector2D(self.x + vector2.x, self.y + vector2.y)
    
    def escalar(self, k):
        return [self.x*k, self.y*k]
    
    def resta_vector(self, vector2):
        return Vector2D(self.x - vector2.x, self.y - vector2.y)
    
    def producto_punto(self, vector2):
        return self.x * vector2.x + self.y * vector2.y

vector1 = Vector2D(1,1)
vector2 = Vector2D(2,2)

print(f'El modulo de vector1 en 2D es: {vector1.modulo()}')
suma = vector1.sumar_vector(vector2)
print(f'El nuevo vector de la suma de vector1 y vector2 es igual a: ({suma.x}, {suma.y})')
escalar = int(input(f'Ingresar escalar por cual quieres multiplicar vector1: '))
print(f'El vector1 multiplicado por {escalar} es igual a {vector1.escalar(escalar)}')
resta = vector1.resta_vector(vector2)
print(f'El nuevo vector de la resta de vector1 y vector2 es igual a: ({resta.x}, {resta.y})')
print(f'El producto punto entre vector1 y vector2 es {vector1.producto_punto(vector2)}')