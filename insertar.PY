import psycopg2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Función para insertar datos en la base de datos
def insertar_juego():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    consola = entry_consola.get()
    ano_de_lanzamiento = entry_ano.get()
    numero_de_jugadores = entry_jugadores.get()
    
    if not nombre or not descripcion or not consola or not ano_de_lanzamiento or not numero_de_jugadores or not image_path:
        messagebox.showerror("Error", "Por favor, completa todos los campos y selecciona una imagen.")
        return

    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        conn = psycopg2.connect("dbname=test1 user=postgres password=123456 host=localhost")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO juegos (Nombre, Descripcion, Consola, Ano_de_lanzamiento, Numero_de_jugadores, Imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, descripcion, consola, ano_de_lanzamiento, numero_de_jugadores, image_data))

        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Éxito", "Juego insertado exitosamente.")
        limpiar_campos()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al insertar el juego: {e}")

# Función para seleccionar la imagen
def seleccionar_imagen():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Imagen JPG", "*.jpg"), ("Imagen PNG", "*.png")])
    if image_path:
        image = Image.open(image_path)
        image.thumbnail((150, 150))
        img = ImageTk.PhotoImage(image)
        label_imagen.config(image=img)
        label_imagen.image = img

# Función para limpiar los campos de texto
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_consola.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_jugadores.delete(0, tk.END)
    label_imagen.config(image='')

# Crear la ventana principal
root = tk.Tk()
root.title("Insertar Juego")

# Variables para almacenar la ruta de la imagen
image_path = None

# Crear etiquetas y campos de entrada
label_nombre = tk.Label(root, text="Nombre:")
label_nombre.grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

label_descripcion = tk.Label(root, text="Descripción:")
label_descripcion.grid(row=1, column=0)
entry_descripcion = tk.Entry(root)
entry_descripcion.grid(row=1, column=1)

label_consola = tk.Label(root, text="Consola:")
label_consola.grid(row=2, column=0)
entry_consola = tk.Entry(root)
entry_consola.grid(row=2, column=1)

label_ano = tk.Label(root, text="Año de Lanzamiento:")
label_ano.grid(row=3, column=0)
entry_ano = tk.Entry(root)
entry_ano.grid(row=3, column=1)

label_jugadores = tk.Label(root, text="Número de Jugadores:")
label_jugadores.grid(row=4, column=0)
entry_jugadores = tk.Entry(root)
entry_jugadores.grid(row=4, column=1)

# Botón para seleccionar imagen
btn_seleccionar_imagen = tk.Button(root, text="Seleccionar Imagen", command=seleccionar_imagen)
btn_seleccionar_imagen.grid(row=5, column=0, columnspan=2)

# Label para mostrar la imagen seleccionada
label_imagen = tk.Label(root)
label_imagen.grid(row=6, column=0, columnspan=2)

# Botón para insertar juego en la base de datos
btn_insertar = tk.Button(root, text="Insertar Juego", command=insertar_juego)
btn_insertar.grid(row=7, column=0, columnspan=2)

# Iniciar la aplicación
root.mainloop()
