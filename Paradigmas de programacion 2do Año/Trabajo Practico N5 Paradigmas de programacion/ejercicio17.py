import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AppLiquidacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Liquidador de Sueldos")
        
        # --- Frame para los Entradas ---
        frame_inputs = ttk.Frame(self.root, padding="10")
        frame_inputs.pack()
        
        # Diccionario para valores base de categorías
        self.valores_categoria = {'A': 5000, 'B': 7000, 'C': 9000}

        # --- Fila 1: Antigüedad ---
        ttk.Label(frame_inputs, text="Antigüedad (años):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_antiguedad = ttk.Entry(frame_inputs, width=20)
        self.entry_antiguedad.grid(row=0, column=1)

        # --- Fila 2: Categoría ---
        ttk.Label(frame_inputs, text="Categoría:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_categoria = ttk.Combobox(
            frame_inputs, 
            values=list(self.valores_categoria.keys()), 
            width=17,
            state="readonly"
        )
        self.combo_categoria.grid(row=1, column=1)
        self.combo_categoria.current(0) # Seleccionar 'A' por defecto

        # --- Fila 3: Horas Trabajadas ---
        ttk.Label(frame_inputs, text="Horas Trabajadas:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_horas = ttk.Entry(frame_inputs, width=20)
        self.entry_horas.grid(row=2, column=1)

        # --- Fila 4: Valor por Hora ---
        ttk.Label(frame_inputs, text="Valor por Hora (ARS):").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_valor_hora = ttk.Entry(frame_inputs, width=20)
        self.entry_valor_hora.grid(row=3, column=1)

        # --- Fila 5: Horas Extras ---
        ttk.Label(frame_inputs, text="Horas Extras:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_horas_extras = ttk.Entry(frame_inputs, width=20)
        self.entry_horas_extras.grid(row=4, column=1)

        # --- Fila 6: Valor Hora Extra ---
        ttk.Label(frame_inputs, text="Valor por Hora Extra (ARS):").grid(row=5, column=0, sticky="w", pady=5)
        self.entry_valor_extra = ttk.Entry(frame_inputs, width=20)
        self.entry_valor_extra.grid(row=5, column=1)

        # --- Fila 7: Otros Beneficios ---
        ttk.Label(frame_inputs, text="Otros Beneficios (ARS):").grid(row=6, column=0, sticky="w", pady=5)
        self.entry_beneficios = ttk.Entry(frame_inputs, width=20)
        self.entry_beneficios.grid(row=6, column=1)

        # --- Botón de Cálculo ---
        self.btn_calcular = ttk.Button(
            self.root, 
            text="Calcular Sueldo", 
            command=self.calcular_sueldo
        )
        self.btn_calcular.pack(pady=10)

        # --- Frame de Resultados ---
        frame_resultados = ttk.Frame(self.root, padding="10")
        frame_resultados.pack()
        
        # Etiquetas para mostrar resultados
        self.lbl_bruto = ttk.Label(frame_resultados, text="Sueldo Bruto: ARS 0.00", font=("Arial", 10))
        self.lbl_bruto.pack(anchor="w")
        self.lbl_jubilacion = ttk.Label(frame_resultados, text="Aporte Jubilatorio (11%): ARS 0.00", font=("Arial", 10))
        self.lbl_jubilacion.pack(anchor="w")
        self.lbl_obra_social = ttk.Label(frame_resultados, text="Obra Social (3%): ARS 0.00", font=("Arial", 10))
        self.lbl_obra_social.pack(anchor="w")
        self.lbl_sindicato = ttk.Label(frame_resultados, text="Aporte Sindical (2%): ARS 0.00", font=("Arial", 10))
        self.lbl_sindicato.pack(anchor="w")
        self.lbl_total_desc = ttk.Label(frame_resultados, text="Descuentos Totales: ARS 0.00", font=("Arial", 10))
        self.lbl_total_desc.pack(anchor="w", pady=(5,0))
        self.lbl_neto = ttk.Label(frame_resultados, text="Sueldo Neto: ARS 0.00", font=("Arial", 12, "bold"))
        self.lbl_neto.pack(anchor="w", pady=(5,0))

    def calcular_sueldo(self):
        try:
            # 1. Obtener todos los valores de los Entry
            antiguedad = int(self.entry_antiguedad.get())
            categoria = self.combo_categoria.get()
            horas_trab = float(self.entry_horas.get())
            valor_hora = float(self.entry_valor_hora.get())
            horas_ext = float(self.entry_horas_extras.get())
            valor_ext = float(self.entry_valor_extra.get())
            beneficios = float(self.entry_beneficios.get())

            # 2. Cálculos según el enunciado
            
            # Sueldo Base [cite: 115]
            valor_base_cat = self.valores_categoria[categoria]
            sueldo_base = valor_base_cat + (antiguedad * 200)
            
            # Sueldo Normal y Extra
            sueldo_normal = horas_trab * valor_hora
            sueldo_extra = horas_ext * valor_ext
            
            # Sueldo Bruto [cite: 118]
            sueldo_bruto = sueldo_base + sueldo_normal + sueldo_extra + beneficios
            
            # Descuentos
            aporte_jub = sueldo_bruto * 0.11
            obra_social = sueldo_bruto * 0.03
            aporte_sind = sueldo_bruto * 0.02
            descuentos_totales = aporte_jub + obra_social + aporte_sind
            
            # Sueldo Neto [cite: 123]
            sueldo_neto = sueldo_bruto - descuentos_totales

            # 3. Actualizar etiquetas de resultados (formateo con 2 decimales)
            self.lbl_bruto.config(text=f"Sueldo Bruto: ARS {sueldo_bruto:.2f}")
            self.lbl_jubilacion.config(text=f"Aporte Jubilatorio (11%): ARS {aporte_jub:.2f}")
            self.lbl_obra_social.config(text=f"Obra Social (3%): ARS {obra_social:.2f}")
            self.lbl_sindicato.config(text=f"Aporte Sindical (2%): ARS {aporte_sind:.2f}")
            self.lbl_total_desc.config(text=f"Descuentos Totales: ARS {descuentos_totales:.2f}")
            self.lbl_neto.config(text=f"Sueldo Neto: ARS {sueldo_neto:.2f}")

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos en todos los campos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")

# --- Bloque principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppLiquidacion(root)
    root.mainloop()