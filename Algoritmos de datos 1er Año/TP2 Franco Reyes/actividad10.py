def return_file_name_modified(file_name):
    file_name_modified = ""
    for caracter in file_name:
        if caracter == " ":
            file_name_modified += "_"
        elif caracter == ".":
            file_name_modified += "#."
        else:
            file_name_modified += caracter
    return file_name_modified

file_name = input("Ingresa el nombre del archivo: ")

file_name_modified = return_file_name_modified(file_name)
print("Nombre modificado:", file_name_modified)
