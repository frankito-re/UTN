def give_multiplication_table(n):
    multiplicated = 1
    while multiplicated <= 10:
        print(f'Numero multiplicado por {multiplicated}: {n*multiplicated}')
        multiplicated+=1
    
give_multiplication_table(4)