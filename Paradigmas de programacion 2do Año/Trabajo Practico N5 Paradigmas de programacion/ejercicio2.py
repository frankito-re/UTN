import tkinter as tk
from tkinter import ttk

class AppSaludador:
    def __init__(self, root):
        self.root = root
        self.root.title("Saludador personal")
        self.root.geometry("300x200")

        # 1. Etiqueta para indicar qué ingresar
        self.lbl_prompt = ttk.Label(self.root, text="Ingresa tu nombre:")
        self.lbl_prompt.pack(pady=5)

        # 2. Entrada de texto (Entry)
        self.entry_nombre = ttk.Entry(self.root, width=30)
        self.entry_nombre.pack(pady=5)

        # 3. Botón para saludar
        self.btn_saludar = ttk.Button(
            self.root, 
            text="Saludar", 
            command=self.saludar_personal
        )
        self.btn_saludar.pack(pady=10)

        # 4. Etiqueta para el resultado
        self.lbl_resultado = ttk.Label(self.root, text="", font=("Arial", 14))
        self.lbl_resultado.pack()

    def saludar_personal(self):
        # 1. Obtenemos el texto del widget 'Entry'
        nombre = self.entry_nombre.get()
        
        # 2. Verificamos que no esté vacío (opcional pero buena práctica)
        if nombre:
            saludo = f"Hola, {nombre}"
            # 3. Actualizamos la etiqueta de resultado
            self.lbl_resultado.config(text=saludo)
        else:
            self.lbl_resultado.config(text="Por favor, ingresa un nombre")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppSaludador(root)
    root.mainloop()