def num_sum(n):
    if n == 0:
        return 1
    else:
        return n + num_sum(n - 1)
    
print(num_sum(5) - 1)