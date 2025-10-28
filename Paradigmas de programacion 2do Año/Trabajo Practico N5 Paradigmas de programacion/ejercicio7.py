import tkinter as tk
from tkinter import ttk

class AppLista:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("300x350")

        # --- Frame para la entrada y el botón ---
        frame_controles = ttk.Frame(self.root)
        frame_controles.pack(pady=10)

        # 1. Entrada de texto
        self.entry_tarea = ttk.Entry(frame_controles, width=20)
        self.entry_tarea.pack(side="left", padx=5)

        # 2. Botón para agregar
        self.btn_agregar = ttk.Button(
            frame_controles, 
            text="Agregar", 
            command=self.agregar_item
        )
        self.btn_agregar.pack(side="left")

        # 3. Listbox para mostrar los ítems
        self.listbox_tareas = tk.Listbox(self.root, width=40, height=15)
        self.listbox_tareas.pack(pady=10, padx=10)

    def agregar_item(self):
        # 1. Obtenemos el texto del Entry
        item = self.entry_tarea.get()

        # 2. Verificamos que no esté vacío
        if item:
            # 3. Insertamos el item al final (tk.END) de la Listbox
            self.listbox_tareas.insert(tk.END, item)
            
            # 4. (Opcional) Borramos el contenido del Entry para el próximo item
            self.entry_tarea.delete(0, tk.END)

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppLista(root)
    root.mainloop()