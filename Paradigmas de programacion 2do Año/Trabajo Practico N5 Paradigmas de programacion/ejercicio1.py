import tkinter as tk
from tkinter import ttk

class AppHolaMundo:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi primer app")
        self.root.geometry("300x150")

        self.btn_saludar = ttk.Button(
            self.root, 
            text="Saludar", 
            command=self.mostrar_saludo
        )
        self.btn_saludar.pack(pady=20) 

        self.lbl_saludo = ttk.Label(self.root, text="", font=("Arial", 14))
        self.lbl_saludo.pack()

    def mostrar_saludo(self):
        self.lbl_saludo.config(text="¡Hola, mundo!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppHolaMundo(root)
    root.mainloop()