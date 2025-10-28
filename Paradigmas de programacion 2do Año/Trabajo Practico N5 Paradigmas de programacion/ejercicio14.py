import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AppFormValidado:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario con Validación")
        self.root.geometry("350x300")

        # --- Nombre ---
        ttk.Label(self.root, text="Nombre:").pack()
        self.entry_nombre = ttk.Entry(self.root, width=40)
        self.entry_nombre.pack()

        # --- Edad ---
        ttk.Label(self.root, text="Edad:").pack()
        self.entry_edad = ttk.Entry(self.root, width=40)
        self.entry_edad.pack()

        # --- Email ---
        ttk.Label(self.root, text="Email:").pack()
        self.entry_email = ttk.Entry(self.root, width=40)
        self.entry_email.pack()

        # --- Contraseña ---
        ttk.Label(self.root, text="Contraseña (mín 6 caracteres):").pack()
        self.entry_pass = ttk.Entry(self.root, width=40, show="*")
        self.entry_pass.pack()

        # --- Botón Registrar ---
        self.btn_registrar = ttk.Button(
            self.root, 
            text="Registrar", 
            command=self.validar_y_registrar
        )
        self.btn_registrar.pack(pady=20)
        
        # --- Etiqueta para mensajes de error ---
        self.lbl_error = ttk.Label(self.root, text="", foreground="red")
        self.lbl_error.pack()

    def validar_y_registrar(self):
        # 1. Reseteamos el mensaje de error
        self.lbl_error.config(text="")

        # 2. Obtenemos los datos
        nombre = self.entry_nombre.get()
        edad_str = self.entry_edad.get()
        email = self.entry_email.get()
        password = self.entry_pass.get()

        # --- 3. Proceso de Validación ---
        
        # Validación de campos vacíos
        if not nombre or not edad_str or not email or not password:
            self.lbl_error.config(text="Error: Todos los campos son obligatorios.")
            return

        # Validación de Edad (numérica) [cite: 66]
        if not edad_str.isdigit():
            self.lbl_error.config(text="Error: La edad debe ser un número.")
            return
            
        edad = int(edad_str)
        if edad < 18:
            self.lbl_error.config(text="Error: Debes ser mayor de edad.")
            return

        # Validación de Email (formato simple) [cite: 66]
        if "@" not in email or "." not in email:
            self.lbl_error.config(text="Error: Formato de email inválido.")
            return
            
        # Validación de Contraseña (largo) [cite: 66]
        if len(password) < 6:
            self.lbl_error.config(text="Error: La contraseña debe tener al menos 6 caracteres.")
            return

        # --- 4. Éxito ---
        self.lbl_error.config(text="") # Limpiamos errores
        messagebox.showinfo(
            "Registro Exitoso", 
            f"¡Bienvenido, {nombre}!\nRegistro completado."
        )

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppFormValidado(root)
    root.mainloop()