# Un almacen tiene capacidad para apilar n contenedores. Cada contenedor tiene un numero
# de identificacion. Cuando se desea retirar un contenedor especıfico, deben retirarse primero
# los contenedores que estan encima de el y colocarlos en otra pila, efectuar el retiro y
# regresarlos. Codifique los metodos push() y pop() para gestionar los contenedores.

def push(stack, container):
    stack.append(container)

def pop(stack):
    if not stack:
        return None
    return stack.pop()

def container_stack(stack, ide):
    stack_2 = []

    # Mover contenedores de stack a stack_2 hasta encontrar el contenedor deseado
    while stack:
        top_container = pop(stack)
        if top_container == ide:
            break
        push(stack_2, top_container)

    # Regresar los contenedores de stack_2 a la pila original
    while stack_2:
        push(stack, pop(stack_2))

    return stack

print(container_stack(['a', 'b', 'c', 'd'], 'b'))