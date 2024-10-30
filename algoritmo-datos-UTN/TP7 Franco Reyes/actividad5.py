# Lea una cadena y determine si los sımbolos ( ) estan correctamente balanceados. Si no lo
# estan muestre el error indicando el sımbolo faltante.

def balance_verify(string:str):
    stack = []
    for letter in string:
        if letter == '(':
            stack.append(letter)
        elif letter == ')':
            if len(stack) == 0:
                return "Error: falta un '(' para balancear"
            stack.pop()
    
    if not stack:
        return "Los paréntesis están correctamente balanceados"
    else:
        return "Error: falta un ')' para balancear"

print(balance_verify('((a + b) * (c - d))'))