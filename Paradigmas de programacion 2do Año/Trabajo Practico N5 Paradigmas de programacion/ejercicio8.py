import tkinter as tk
from tkinter import ttk
from tkinter import messagebox # Importamos el módulo de ventanas emergentes

class AppFormulario:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario de Registro")
        self.root.geometry("350x250")

        # --- Campo Nombre ---
        ttk.Label(self.root, text="Nombre:").pack()
        self.entry_nombre = ttk.Entry(self.root, width=40)
        self.entry_nombre.pack()

        # --- Campo Apellido ---
        ttk.Label(self.root, text="Apellido:").pack()
        self.entry_apellido = ttk.Entry(self.root, width=40)
        self.entry_apellido.pack()

        # --- Campo Email ---
        ttk.Label(self.root, text="Email:").pack()
        self.entry_email = ttk.Entry(self.root, width=40)
        self.entry_email.pack()

        # --- Campo Contraseña ---
        ttk.Label(self.root, text="Contraseña:").pack()
        self.entry_pass = ttk.Entry(self.root, width=40, show="*") # 'show' oculta la contraseña
        self.entry_pass.pack()

        # --- Botón Enviar ---
        self.btn_enviar = ttk.Button(
            self.root, 
            text="Enviar", 
            command=self.enviar_formulario
        )
        self.btn_enviar.pack(pady=20)

    def enviar_formulario(self):
        # 1. Recolectamos los datos de todos los Entry
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        email = self.entry_email.get()
        password = self.entry_pass.get() # No es buena práctica, pero sigue el enunciado

        # 2. Creamos el mensaje de confirmación
        mensaje = f"Datos Recibidos:\n\n"
        mensaje += f"Nombre: {nombre}\n"
        mensaje += f"Apellido: {apellido}\n"
        mensaje += f"Email: {email}\n"

        # 3. Mostramos el mensaje en una ventana emergente
        messagebox.showinfo("Confirmación", mensaje)

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppFormulario(root)
    root.mainloop()