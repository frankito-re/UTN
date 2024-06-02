def capital_letter(string: str):
    words = string.split()
    
    capitalized_words = []
    for word in words:
        upper_letter = word[0].upper() + word[1:]
        capitalized_words.append(upper_letter)
        
    capitalized_string = " ".join(capitalized_words)
    print(capitalized_string)
    
capital_letter('hola como estas?')