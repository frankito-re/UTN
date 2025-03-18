def binary_compare(binary: int):
    ones_n = str(binary).count('1')
    zeros_n = str(binary).count('0')
    print(ones_n == zeros_n)
    
binary_compare(10100011)