import tkinter as tk
from tkinter import ttk

class AppConversor:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Temperatura")
        self.root.geometry("300x200")

        # --- Widgets de entrada ---
        ttk.Label(self.root, text="Grados Celsius:").pack(pady=5)
        self.entry_celsius = ttk.Entry(self.root)
        self.entry_celsius.pack(pady=5)

        # --- Botón ---
        self.btn_convertir = ttk.Button(
            self.root, 
            text="Convertir", 
            command=self.convertir_a_fahrenheit
        )
        self.btn_convertir.pack(pady=10)

        # --- Resultado ---
        self.lbl_fahrenheit = ttk.Label(self.root, text="--- °F", font=("Arial", 16))
        self.lbl_fahrenheit.pack(pady=10)

    def convertir_a_fahrenheit(self):
        try:
            # 1. Obtenemos y convertimos el valor de Celsius
            celsius = float(self.entry_celsius.get())

            # 2. Aplicamos la fórmula de conversión
            fahrenheit = (celsius * 9/5) + 32

            # 3. Actualizamos la etiqueta
            # Usamos :.1f para formatear el número y mostrar solo 1 decimal
            self.lbl_fahrenheit.config(text=f"{fahrenheit:.1f} °F")

        except ValueError:
            # Manejamos el error si el ingreso no es numérico
            self.lbl_fahrenheit.config(text="Valor inválido")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppConversor(root)
    root.mainloop()