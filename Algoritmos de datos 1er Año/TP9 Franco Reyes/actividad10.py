class Libro:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
    
    def __repr__(self):
        return f"{self.titulo} por {self.autor}, {self.paginas} páginas"

#Aca utilizo el algoritmo de ordenamiento de burbuja: bubble sort
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j].paginas > lista[j+1].paginas:
                lista[j], lista[j+1] = lista[j+1], lista[j]

# Utilizo una lista de libros
libros = [
    Libro("1984", "George Orwell", 328),
    Libro("Cien años de soledad", "Gabriel García Márquez", 417),
    Libro("El principito", "Antoine de Saint-Exupéry", 96),
    Libro("Don Quijote de la Mancha", "Miguel de Cervantes", 863),
    Libro("Fahrenheit 451", "Ray Bradbury", 158)
]

# Ordeno la lista de libros por número de páginas
bubble_sort(libros)

# Imprimo la lista de libros ordenados por páginas
for libro in libros:
    print(libro)