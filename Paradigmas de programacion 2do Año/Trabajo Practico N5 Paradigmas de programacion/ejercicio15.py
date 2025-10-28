import tkinter as tk
from tkinter import ttk

class AppTodoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")

        # --- Frame para la entrada y botón ---
        frame_controles = ttk.Frame(self.root)
        frame_controles.pack(pady=10)

        self.entry_tarea = ttk.Entry(frame_controles, width=30)
        self.entry_tarea.pack(side="left", padx=5)
        
        self.btn_agregar = ttk.Button(
            frame_controles, 
            text="Agregar Tarea", 
            command=self.agregar_tarea
        )
        self.btn_agregar.pack(side="left")

        # --- Frame para mostrar las tareas ---
        # Usamos un Frame que se actualizará con las tareas
        self.frame_tareas = ttk.Frame(self.root)
        self.frame_tareas.pack(fill="both", expand=True, padx=10, pady=10)

    def agregar_tarea(self):
        tarea_texto = self.entry_tarea.get()
        if not tarea_texto:
            return # No agregar tareas vacías
            
        # 1. Creamos un Frame para la fila de la tarea (Checkbutton + Botón Borrar)
        task_frame = ttk.Frame(self.frame_tareas)
        
        # 2. Variable para el estado del Checkbutton
        var = tk.IntVar()
        
        # 3. Checkbutton
        cb = ttk.Checkbutton(
            task_frame, 
            text=tarea_texto, 
            variable=var, 
            onvalue=1, 
            offvalue=0
        )
        cb.pack(side="left")

        # 4. Botón Eliminar (opcional, como dice el enunciado) [cite: 70]
        # Usamos lambda para pasar el 'task_frame' que debe ser destruido
        btn_eliminar = ttk.Button(
            task_frame, 
            text="Eliminar", 
            command=lambda f=task_frame: f.destroy()
        )
        btn_eliminar.pack(side="right", padx=5)

        # 5. Añadimos el frame de la tarea al frame principal
        task_frame.pack(fill="x") # 'fill="x"' hace que ocupe todo el ancho
        
        # Limpiamos la entrada
        self.entry_tarea.delete(0, tk.END)

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppTodoList(root)
    root.mainloop()