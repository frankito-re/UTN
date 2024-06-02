frase = "Hola"

def f():
    frase = "Es un lindo dia"
    print(frase)

# El codigo imprimira "Hola", porque nunca es llamada
# El alcance de la variable frase es global, pero el alcance de la variable reasignada dentro de la funcion, el alcance solo es dentro de la funcion