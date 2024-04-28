valid_names = ['Juan', 'María', 'Pedro', 'Ana', 'Luis']

user_name = input("Ingrese su nombre: ")

if user_name in valid_names:
    print(f"Bienvenido, {user_name}!")
else:
    print("Nombre de usuario no válido.")