# Nombre alumno: Franco Genaro Reyes

# Crea una ventana con Tkinter que muestre una etiqueta (Label) con el texto "¡Hola,
# mundo!" al presionar un boton.
import tkinter as tk

root = tk.Tk()
root.title("Ventana de prueba")
root.geometry("300x200")  # Fijamos tamaño para que sea más visible

label = tk.Label(
    root,
    text="¡Hola mundo!",
    bg="red",
    fg="white",
    font=("Arial", 16),
    width=20,
    height=2,
    relief="solid",  # Borde para que se note
    bd=2              # Grosor del borde
)
label.pack(pady=20)

root.mainloop()