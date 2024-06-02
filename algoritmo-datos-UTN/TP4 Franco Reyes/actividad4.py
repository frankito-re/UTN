x = 3
def f():
    y = x + 1
    print(x)
    def g():
        x = 1
        print(y)
        print(x)
    g()
f()

# El alcance de la variable "x" es global
# El alcance de la variable "y" es solo llamable en al funcion "f()"
# El alcance de la variable "x" reasignada es global, pero solo va ser reasignada si se llama a la funcion "g()"