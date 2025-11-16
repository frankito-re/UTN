# a) Máximo de dos números
maximo(A, B, A) :- A >= B.
maximo(A, B, B) :- B > A.

# b) Área de un círculo (A = pi * r^2)
area_circulo(Radio, Area) :-
    Area is pi * Radio^2.

# c) Perímetro de un rectángulo (P = 2b + 2h)
perim_rect(Base, Altura, Perimetro) :-
    Perimetro is 2 * Base + 2 * Altura.

# d) Volumen de una esfera (V = 4/3 * pi * r^3)
vol_esfera(Radio, Volumen) :-
    Volumen is (4/3) * pi * Radio^3.

# e) Volumen de un cono (V = 1/3 * pi * r^2 * h)
vol_cono(Radio, Altura, Volumen) :-
    Volumen is (1/3) * pi * (Radio^2) * Altura.

# f) Velocidad MRUV (Vf = V0 + a*t)
velocidad_mruv(V0, A, T, VF) :-
    VF is V0 + A * T.

# g) Módulo de un vector de 3 componentes
modulo_vector3(X, Y, Z, Modulo) :-
    Modulo is sqrt(X^2 + Y^2 + Z^2).