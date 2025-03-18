def list_sum(num_list):
    # Caso base: si la lista está vacía, retornar 0
    if not num_list:
        return 0
    # Caso recursivo: sumar el primer elemento con la suma del resto de la lista
    else:
        return num_list[0] + list_sum(num_list[1:])

print(list_sum([1, 5, 6]))

test_list = [1, 6 , 2]
print(test_list[1:])
