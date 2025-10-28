import tkinter as tk
from tkinter import ttk

class AppContador:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador")
        self.root.geometry("300x200")

        # 1. Variable de estado para guardar el número
        self.contador = 0

        # 2. Etiqueta para mostrar el número
        self.lbl_numero = ttk.Label(
            self.root, 
            text=str(self.contador), 
            font=("Arial", 30)
        )
        self.lbl_numero.pack(pady=20)

        # 3. Botón de sumar
        self.btn_sumar = ttk.Button(
            self.root, 
            text="Sumar +", 
            command=self.sumar
        )
        self.btn_sumar.pack(side="left", expand=True, padx=10) # 'side' para ponerlos uno al lado del otro

        # 4. Botón de restar
        self.btn_restar = ttk.Button(
            self.root, 
            text="Restar -", 
            command=self.restar
        )
        self.btn_restar.pack(side="right", expand=True, padx=10)

    def sumar(self):
        # Aumentamos el contador
        self.contador += 1
        # Actualizamos la etiqueta
        self.actualizar_label()

    def restar(self):
        # Disminuimos el contador
        self.contador -= 1
        # Actualizamos la etiqueta
        self.actualizar_label()

    def actualizar_label(self):
        # Función auxiliar para no repetir código
        self.lbl_numero.config(text=str(self.contador))

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppContador(root)
    root.mainloop()