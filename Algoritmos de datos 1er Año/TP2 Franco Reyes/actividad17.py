film_names = []

for i in range(10):
    film_name = input(f"Ingrese el nombre de la película {i + 1}: ")
    film_names.append(film_name)
    
while True:
    try:
        film_number = int(input("Ingrese un número del 1 al 10: "))
        if 1 <= film_number <= 10:
            break
        else:
            print("El número debe estar entre 1 y 10. Inténtelo de nuevo.")
    except ValueError:
        print("Debe ingresar un número entero. Inténtelo de nuevo.")
        
selected_film_name = film_names[film_number - 1]
print(f"La película número {film_number} es: {selected_film_name}")
