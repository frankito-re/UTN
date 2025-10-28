import tkinter as tk
from tkinter import ttk

class AppIMC:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de IMC")
        self.root.geometry("300x350")

        # --- Peso ---
        ttk.Label(self.root, text="Peso (en kg):").pack(pady=5)
        self.entry_peso = ttk.Entry(self.root, width=15)
        self.entry_peso.pack(pady=5)

        # --- Altura ---
        ttk.Label(self.root, text="Altura (en metros, ej: 1.75):").pack(pady=5)
        self.entry_altura = ttk.Entry(self.root, width=15)
        self.entry_altura.pack(pady=5)

        # --- Botón ---
        self.btn_calcular = ttk.Button(
            self.root, 
            text="Calcular IMC", 
            command=self.calcular_imc
        )
        self.btn_calcular.pack(pady=20)

        # --- Etiquetas de Resultado ---
        self.lbl_resultado_imc = ttk.Label(self.root, text="Tu IMC es:", font=("Arial", 14))
        self.lbl_resultado_imc.pack(pady=10)

        self.lbl_clasificacion = ttk.Label(self.root, text="---", font=("Arial", 16, "bold"))
        self.lbl_clasificacion.pack(pady=10)

    def calcular_imc(self):
        try:
            peso = float(self.entry_peso.get())
            altura = float(self.entry_altura.get())

            if altura <= 0:
                self.lbl_resultado_imc.config(text="Altura debe ser > 0")
                self.lbl_clasificacion.config(text="Error", foreground="red")
                return

            # Fórmula del IMC
            imc = peso / (altura ** 2)

            # Mostramos el resultado numérico
            self.lbl_resultado_imc.config(text=f"Tu IMC es: {imc:.2f}")

            # Clasificamos el resultado
            self.clasificar_imc(imc)

        except ValueError:
            self.lbl_resultado_imc.config(text="Error: Ingresa números válidos")
            self.lbl_clasificacion.config(text="Error", foreground="red")

    def clasificar_imc(self, imc):
        # Clasificamos y cambiamos el color de la etiqueta
        if imc < 18.5:
            self.lbl_clasificacion.config(text="Bajo Peso", foreground="blue")
        elif 18.5 <= imc < 24.9:
            self.lbl_clasificacion.config(text="Peso Normal", foreground="green")
        elif 25 <= imc < 29.9:
            self.lbl_clasificacion.config(text="Sobrepeso", foreground="orange")
        else: # imc >= 30
            self.lbl_clasificacion.config(text="Obesidad", foreground="red")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppIMC(root)
    root.mainloop()