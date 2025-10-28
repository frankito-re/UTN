import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

class AppBuscaLetras:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memoria")

        # --- Datos del juego ---
        # 8 pares de letras para una grilla 4x4
        letras = list('AABBCCDDEEFFGGHH')
        random.shuffle(letras)
        
        # Convertimos la lista plana en una grilla 4x4
        self.grilla_letras = []
        for i in range(4):
            fila = letras[i*4 : (i+1)*4]
            self.grilla_letras.append(fila)

        # --- Estado del juego ---
        self.botones = [] # Para guardar los widgets Button
        self.primer_click = None # Guarda la (fila, col) del primer click
        self.clicks_bloqueados = False # Para evitar 3 clicks rápidos
        self.aciertos = 0 # Contador de pares encontrados

        # --- Creación de la grilla de botones ---
        frame_juego = ttk.Frame(self.root)
        frame_juego.pack(pady=10, padx=10)

        for r in range(4):
            fila_botones = []
            for c in range(4):
                # Usamos lambda para pasar los argumentos 'r' y 'c' al hacer click
                btn = tk.Button(
                    frame_juego, 
                    text="", 
                    width=6, 
                    height=3,
                    font=("Arial", 14, "bold"),
                    command=lambda fila=r, col=c: self.on_click_boton(fila, col)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                fila_botones.append(btn)
            self.botones.append(fila_botones)

    def on_click_boton(self, fila, col):
        # Si los clicks están bloqueados (esperando el temporizador) o la carta ya está acertada, no hacer nada
        if self.clicks_bloqueados or self.botones[fila][col]['state'] == 'disabled':
            return

        # Obtener el botón y la letra
        boton_clicado = self.botones[fila][col]
        letra = self.grilla_letras[fila][col]
        
        # Mostrar la letra
        boton_clicado.config(text=letra)

        if self.primer_click is None:
            # --- Es el primer click ---
            self.primer_click = (fila, col)
        else:
            # --- Es el segundo click ---
            self.clicks_bloqueados = True # Bloquear más clicks
            fila1, col1 = self.primer_click
            
            # Evitar click en la misma carta
            if (fila, col) == (fila1, col1):
                self.clicks_bloqueados = False
                return

            letra1 = self.grilla_letras[fila1][col1]
            boton1 = self.botones[fila1][col1]

            if letra1 == letra:
                # --- ¡Es un acierto! ---
                boton_clicado.config(state='disabled')
                boton1.config(state='disabled')
                self.aciertos += 1
                self.primer_click = None
                self.clicks_bloqueados = False
                
                # Verificar si ganó
                if self.aciertos == 8:
                    messagebox.showinfo("¡Felicidades!", "¡Ganaste el juego!")
            else:
                # --- No es acierto ---
                # Esperar 1 segundo (1000 ms) antes de llamar a 'ocultar_cartas'
                self.root.after(
                    1000, 
                    self.ocultar_cartas, 
                    boton_clicado, 
                    boton1
                )

    def ocultar_cartas(self, boton2, boton1):
        # Ocultar las letras
        boton2.config(text="")
        boton1.config(text="")
        
        # Reiniciar estado
        self.primer_click = None
        self.clicks_bloqueados = False

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppBuscaLetras(root)
    root.mainloop()