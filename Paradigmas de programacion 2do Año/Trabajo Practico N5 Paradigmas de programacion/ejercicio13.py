import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  # Para abrir ventanas de diálogo de archivos
from tkinter import messagebox

class AppBlocDeNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Bloc de Notas")
        self.root.geometry("600x400")

        # --- Frame para los botones ---
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(pady=5)

        self.btn_abrir = ttk.Button(
            frame_botones, 
            text="Abrir", 
            command=self.abrir_archivo
        )
        self.btn_abrir.pack(side="left", padx=5)

        self.btn_guardar = ttk.Button(
            frame_botones, 
            text="Guardar como...", 
            command=self.guardar_archivo
        )
        self.btn_guardar.pack(side="left", padx=5)

        # --- Área de Texto ---
        # 'expand=True' y 'fill="both"' hacen que el widget de texto
        # llene todo el espacio restante de la ventana.
        self.area_texto = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.area_texto.pack(padx=10, pady=10, fill="both", expand=True)

    def abrir_archivo(self):
        # Pide al usuario que elija un archivo
        filepath = filedialog.askopenfilename(
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
        )
        
        if not filepath: # Si el usuario cancela
            return
            
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                contenido = file.read()
                
            # Borra el contenido actual del área de texto
            self.area_texto.delete("1.0", tk.END) 
            # Inserta el contenido del archivo ("1.0" es el inicio del texto)
            self.area_texto.insert("1.0", contenido)
            self.root.title(f"Mini Bloc de Notas - {filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar_archivo(self):
        # Pide al usuario dónde guardar el archivo
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
        )

        if not filepath: # Si el usuario cancela
            return
            
        try:
            # Obtenemos todo el texto del widget Text ("1.0" al final "tk.END")
            contenido = self.area_texto.get("1.0", tk.END)
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(contenido)
            self.root.title(f"Mini Bloc de Notas - {filepath}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppBlocDeNotas(root)
    root.mainloop()