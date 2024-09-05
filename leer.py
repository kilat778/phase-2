import psycopg2
import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import io

# Variables globales para manejar el índice de los registros
resultados = []
indice_actual = 0

# Función para mostrar los datos de un juego específico según el índice
def mostrar_dato(indice):
    if resultados and 0 <= indice < len(resultados):
        row = resultados[indice]
        
        codigo.set(f"Codigo: {row[0]}")
        nombre.set(f"Nombre: {row[1]}")
        descripcion.set(f"Descripcion: {row[2]}")
        consola.set(f"Consola: {row[3]}")
        ano_lanzamiento.set(f"Año de Lanzamiento: {row[4]}")
        num_jugadores.set(f"Número de Jugadores: {row[5]}")

        # Si hay una imagen, mostrarla
        if row[6] is not None:
            image_data = row[6]
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((250, 250))  # Ajustar tamaño de la imagen
            img_tk = ImageTk.PhotoImage(image)
            imagen_label.config(image=img_tk)
            imagen_label.image = img_tk
    else:
        limpiar_campos()

# Función para cargar todos los datos
def mostrar_todos():
    global resultados, indice_actual
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect("dbname=test1 user=postgres password=123456 host=localhost")
        cur = conn.cursor()

        # Consultar todos los datos de la tabla juegos
        cur.execute("SELECT Codigo, Nombre, Descripcion, Consola, Ano_de_lanzamiento, Numero_de_jugadores, Imagen FROM juegos;")
        resultados = cur.fetchall()

        if resultados:
            indice_actual = 0  # Reiniciar el índice
            mostrar_dato(indice_actual)  # Mostrar el primer registro
        else:
            messagebox.showinfo("Información", "No se encontraron datos en la base de datos.")
        
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar los datos: {e}")

# Función para avanzar al siguiente registro
def siguiente():
    global indice_actual
    if indice_actual < len(resultados) - 1:
        indice_actual += 1
        mostrar_dato(indice_actual)
    else:
        messagebox.showinfo("Información", "No hay más registros.")

# Función para retroceder al registro anterior
def anterior():
    global indice_actual
    if indice_actual > 0:
        indice_actual -= 1
        mostrar_dato(indice_actual)
    else:
        messagebox.showinfo("Información", "Este es el primer registro.")

# Función para limpiar los campos de la interfaz
def limpiar_campos():
    codigo.set("Codigo: ")
    nombre.set("Nombre: ")
    descripcion.set("Descripcion: ")
    consola.set("Consola: ")
    ano_lanzamiento.set("Año de Lanzamiento: ")
    num_jugadores.set("Número de Jugadores: ")
    imagen_label.config(image='')

# Configuración de la ventana principal
root = tk.Tk()
root.title("Datos de Juegos")
root.geometry("400x600")

# Variables para mostrar los datos
codigo = tk.StringVar()
nombre = tk.StringVar()
descripcion = tk.StringVar()
consola = tk.StringVar()
ano_lanzamiento = tk.StringVar()
num_jugadores = tk.StringVar()

# Etiquetas para mostrar los datos
tk.Label(root, textvariable=codigo).pack(pady=5)
tk.Label(root, textvariable=nombre).pack(pady=5)
tk.Label(root, textvariable=descripcion).pack(pady=5)
tk.Label(root, textvariable=consola).pack(pady=5)
tk.Label(root, textvariable=ano_lanzamiento).pack(pady=5)
tk.Label(root, textvariable=num_jugadores).pack(pady=5)

# Etiqueta para mostrar la imagen
imagen_label = Label(root)
imagen_label.pack(pady=10)

# Botón para cargar todos los datos
tk.Button(root, text="Mostrar Todos", command=mostrar_todos).pack(pady=20)

# Botones de navegación
tk.Button(root, text="Anterior", command=anterior).pack(side=tk.LEFT, padx=20)
tk.Button(root, text="Siguiente", command=siguiente).pack(side=tk.RIGHT, padx=20)

# Iniciar la interfaz
root.mainloop()
