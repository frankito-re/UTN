import tkinter as tk
from tkinter import ttk
import random # Importamos el módulo random

class AppAdivina:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina el Número")
        self.root.geometry("350x250")

        # 1. Generamos el número secreto (entre 1 y 100) al iniciar la app
        self.numero_secreto = random.randint(1, 100)
        self.intentos = 0

        # --- Widgets ---
        ttk.Label(
            self.root, 
            text="Adivina un número entre 1 y 100", 
            font=("Arial", 14)
        ).pack(pady=10)

        self.entry_numero = ttk.Entry(self.root, width=10)
        self.entry_numero.pack(pady=10)

        self.btn_adivinar = ttk.Button(
            self.root, 
            text="Adivinar", 
            command=self.verificar_numero
        )
        self.btn_adivinar.pack(pady=10)

        self.lbl_pista = ttk.Label(self.root, text="¡Suerte!", font=("Arial", 12))
        self.lbl_pista.pack(pady=10)

    def verificar_numero(self):
        try:
            # 1. Obtenemos y convertimos el número
            guess = int(self.entry_numero.get())
            self.intentos += 1

            # 2. Comparamos el número
            if guess < self.numero_secreto:
                self.lbl_pista.config(text="Demasiado bajo. Intenta de nuevo.")
            elif guess > self.numero_secreto:
                self.lbl_pista.config(text="Demasiado alto. Intenta de nuevo.")
            else:
                self.lbl_pista.config(
                    text=f"¡Acertaste! El número era {self.numero_secreto}. (Intentos: {self.intentos})"
                )
                # Deshabilitamos el botón y la entrada al ganar
                self.btn_adivinar.config(state="disabled")
                self.entry_numero.config(state="disabled")
        
        except ValueError:
            self.lbl_pista.config(text="Error: Debes ingresar un número entero.")
        
        # (Opcional) Limpiamos la entrada después de cada intento
        self.entry_numero.delete(0, tk.END)


# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppAdivina(root)
    root.mainloop()