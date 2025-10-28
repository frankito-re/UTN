import tkinter as tk
from tkinter import ttk

class AppSumadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Sumadora")
        self.root.geometry("300x250")

        # --- Entradas de Número ---
        ttk.Label(self.root, text="Número 1:").pack(pady=5)
        self.entry_num1 = ttk.Entry(self.root)
        self.entry_num1.pack(pady=5)

        ttk.Label(self.root, text="Número 2:").pack(pady=5)
        self.entry_num2 = ttk.Entry(self.root)
        self.entry_num2.pack(pady=5)

        # --- Botón para Calcular ---
        self.btn_sumar = ttk.Button(
            self.root, 
            text="Sumar", 
            command=self.realizar_suma
        )
        self.btn_sumar.pack(pady=10)

        # --- Resultado ---
        self.lbl_resultado = ttk.Label(self.root, text="Resultado:", font=("Arial", 14))
        self.lbl_resultado.pack(pady=10)

    def realizar_suma(self):
        try:
            # 1. Obtenemos los textos de los Entry
            texto_num1 = self.entry_num1.get()
            texto_num2 = self.entry_num2.get()

            # 2. Convertimos los textos a números flotantes (con decimales)
            num1 = float(texto_num1)
            num2 = float(texto_num2)

            # 3. Realizamos la suma
            suma = num1 + num2

            # 4. Actualizamos la etiqueta con el resultado
            self.lbl_resultado.config(text=f"Resultado: {suma}")

        except ValueError:
            # Si el usuario escribe algo que no es un número (ej: "hola"),
            # float() dará un error. Lo capturamos aquí.
            self.lbl_resultado.config(text="Error: Ingrese solo números")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppSumadora(root)
    root.mainloop()