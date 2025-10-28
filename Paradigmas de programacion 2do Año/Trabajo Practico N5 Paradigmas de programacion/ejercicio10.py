import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AppCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Calculadora")
        self.root.geometry("300x400") # Tamaño ajustado para la calculadora
        self.root.resizable(False, False) # Evitar que se cambie de tamaño

        # 1. Pantalla (Entry)
        # 'readonly' para que solo se pueda escribir con los botones
        self.display_var = tk.StringVar()
        self.display = ttk.Entry(
            self.root, 
            textvariable=self.display_var, 
            font=("Arial", 24), 
            justify="right", 
            state="readonly"
        )
        self.display.pack(fill="x", padx=10, pady=10)

        # 2. Frame para los botones
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack()

        # 3. Definimos los botones (texto, fila, columna)
        # 'sticky="nsew"' hace que el botón se expanda para llenar su celda
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
        ]

        # 4. Creamos y ubicamos los botones en la grilla (grid)
        for (text, row, col) in buttons:
            btn = ttk.Button(
                btn_frame, 
                text=text, 
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", ipadx=10, ipady=10)

        # 5. Botón de Igual (=)
        # 'columnspan=4' hace que ocupe las 4 columnas
        btn_equal = ttk.Button(
            btn_frame, 
            text="=", 
            command=self.calcular_resultado
        )
        btn_equal.grid(row=5, column=0, columnspan=4, sticky="nsew", ipady=10)

    def on_button_click(self, char):
        current_text = self.display_var.get()
        
        if char == 'C':
            # 'C' (Clear) borra la pantalla
            self.display_var.set("")
        else:
            # Añade el caracter presionado a la pantalla
            self.display_var.set(current_text + str(char))

    def calcular_resultado(self):
        try:
            # 1. Obtiene la expresión de la pantalla
            expression = self.display_var.get()
            
            # 2. Usa eval() para calcular el resultado
            # ADVERTENCIA: eval() es potente pero inseguro en apps reales
            # Para un trabajo práctico está bien.
            result = eval(expression)
            
            # 3. Muestra el resultado en la pantalla
            self.display_var.set(str(result))
            
        except ZeroDivisionError:
            self.display_var.set("Error: Div / 0")
        except Exception as e:
            # Captura cualquier otro error (ej. "1++2")
            self.display_var.set("Error de sintaxis")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppCalculadora(root)
    root.mainloop()