import tkinter as tk
from tkinter import ttk

class AppPaint:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint")
        
        # 1. Variables de estado
        self.color_dibujo = "black"
        self.last_x = None
        self.last_y = None

        # 2. Frame para botones de control (colores, borrar)
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side="top", fill="x", pady=5)

        ttk.Button(
            control_frame, text="Negro", command=lambda: self.set_color("black")
        ).pack(side="left", padx=5)
        ttk.Button(
            control_frame, text="Rojo", command=lambda: self.set_color("red")
        ).pack(side="left", padx=5)
        ttk.Button(
            control_frame, text="Azul", command=lambda: self.set_color("blue")
        ).pack(side="left", padx=5)
        ttk.Button(
            control_frame, text="Borrar Todo", command=self.clear_canvas
        ).pack(side="right", padx=5)

        # 3. Widget Canvas (el lienzo para dibujar)
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # 4. Binds (Vincular) eventos del mouse a funciones
        # Cuando se mueva el mouse con clic izquierdo, llama a 'paint'
        self.canvas.bind("<B1-Motion>", self.paint)
        # Cuando se suelte el clic, llama a 'reset'
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def set_color(self, new_color):
        # Actualiza el color de dibujo
        self.color_dibujo = new_color

    def clear_canvas(self):
        # Borra todo lo que tenga la etiqueta "linea" (o "all" para todo)
        self.canvas.delete("all")

    def paint(self, event):
        # 'event' contiene la info del mouse (ej. event.x, event.y)
        if self.last_x and self.last_y:
            # Si tenemos un punto anterior, dibujamos una línea
            self.canvas.create_line(
                self.last_x, self.last_y, 
                event.x, event.y, 
                width=3, 
                fill=self.color_dibujo, 
                capstyle=tk.ROUND, # Puntas redondeadas
                smooth=tk.TRUE     # Línea suave
            )
        
        # Actualizamos el último punto
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        # Al soltar el clic, reiniciamos las coordenadas
        # para que el próximo clic inicie una nueva línea
        self.last_x = None
        self.last_y = None

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppPaint(root)
    root.mainloop()