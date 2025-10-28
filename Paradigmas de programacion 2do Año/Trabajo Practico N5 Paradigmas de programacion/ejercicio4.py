import tkinter as tk
from tkinter import ttk

class AppColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Selector de Color")
        self.root.geometry("300x200")

        # 1. Creamos un 'Frame' (marco) para contener los botones
        # Esto nos ayuda a agruparlos visualmente
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=50) # Le damos un padding vertical

        # 2. Botón Rojo
        # Usamos 'lambda' para poder pasar un argumento ('red') a la función 'cambiar_color'
        # Si pusiéramos command=self.cambiar_color("red") se ejecutaría al crear el botón, no al hacer clic
        self.btn_rojo = ttk.Button(
            control_frame, 
            text="Rojo", 
            command=lambda: self.cambiar_color("red")
        )
        self.btn_rojo.pack(side="left", padx=5)

        # 3. Botón Verde
        self.btn_verde = ttk.Button(
            control_frame, 
            text="Verde", 
            command=lambda: self.cambiar_color("green")
        )
        self.btn_verde.pack(side="left", padx=5)

        # 4. Botón Azul
        self.btn_azul = ttk.Button(
            control_frame, 
            text="Azul", 
            command=lambda: self.cambiar_color("blue")
        )
        self.btn_azul.pack(side="left", padx=5)

    def cambiar_color(self, color):
        # Esta función cambia el color de fondo (bg) de la ventana principal
        self.root.configure(bg=color)

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppColorPicker(root)
    root.mainloop()