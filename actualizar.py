import psycopg2
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import io

# Función para seleccionar una imagen desde el sistema de archivos
def seleccionar_imagen():
    global imagen_data
    ruta_imagen = filedialog.askopenfilename(
        title="Seleccionar Imagen",
        filetypes=[("Archivos de imagen", "*.jpg;*.png")]
    )
    
    if ruta_imagen:
        # Leer la imagen seleccionada en binario
        with open(ruta_imagen, 'rb') as f:
            imagen_data = f.read()

        # Mostrar la imagen seleccionada en la interfaz
        image = Image.open(io.BytesIO(imagen_data))
        image = image.resize((150, 150))  # Ajustar el tamaño de la imagen
        img_tk = ImageTk.PhotoImage(image)
        label_imagen.config(image=img_tk)
        label_imagen.image = img_tk

# Función para cargar los datos de un juego en los campos de entrada
def cargar_datos():
    id_juego = entry_id.get()

    if not id_juego:
        messagebox.showerror("Error", "Debe ingresar el ID del juego a actualizar.")
        return

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect("dbname=test1 user=postgres password=123456 host=localhost")
        cur = conn.cursor()

        # Consultar el juego por ID
        cur.execute("SELECT Nombre, Descripcion, Consola, Año_de_lanzamiento, Numero_de_jugadores, Imagen FROM juegos WHERE Codigo = %s;", (id_juego,))
        juego = cur.fetchone()

        if juego:
            # Rellenar los campos con los datos del juego
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, juego[0])
            entry_descripcion.delete(0, tk.END)
            entry_descripcion.insert(0, juego[1])
            entry_consola.delete(0, tk.END)
            entry_consola.insert(0, juego[2])
            entry_ano_lanzamiento.delete(0, tk.END)
            entry_ano_lanzamiento.insert(0, juego[3])
            entry_num_jugadores.delete(0, tk.END)
            entry_num_jugadores.insert(0, juego[4])

            # Mostrar la imagen actual
            if juego[5]:
                global imagen_data
                imagen_data = juego[5]
                image = Image.open(io.BytesIO(imagen_data))
                image = image.resize((150, 150))
                img_tk = ImageTk.PhotoImage(image)
                label_imagen.config(image=img_tk)
                label_imagen.image = img_tk
        else:
            messagebox.showinfo("Información", "No se encontró ningún juego con el ID proporcionado.")
        
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar los datos: {e}")

# Función para actualizar los datos del juego
def actualizar_datos():
    id_juego = entry_id.get()
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    consola = entry_consola.get()
    ano_lanzamiento = entry_ano_lanzamiento.get()
    num_jugadores = entry_num_jugadores.get()

    if not (id_juego and nombre and descripcion and consola and ano_lanzamiento and num_jugadores):
        messagebox.showerror("Error", "Todos los campos deben estar completos.")
        return

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect("dbname=test1 user=postgres password=123456 host=localhost")
        cur = conn.cursor()

        # Actualizar los datos del juego
        cur.execute("""
            UPDATE juegos
            SET Nombre = %s, Descripcion = %s, Consola = %s, Año_de_lanzamiento = %s, Numero_de_jugadores = %s, Imagen = %s
            WHERE Codigo = %s;
        """, (nombre, descripcion, consola, ano_lanzamiento, num_jugadores, imagen_data, id_juego))

        conn.commit()

        messagebox.showinfo("Éxito", "El juego ha sido actualizado correctamente.")

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al actualizar los datos: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Actualizar Datos de Juegos")
root.geometry("500x600")

# Variables
imagen_data = None

# Etiquetas y campos de entrada
tk.Label(root, text="ID del Juego:").pack(pady=5)
entry_id = tk.Entry(root)
entry_id.pack(pady=5)

tk.Button(root, text="Cargar Datos", command=cargar_datos).pack(pady=5)

tk.Label(root, text="Nombre:").pack(pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.pack(pady=5)

tk.Label(root, text="Descripción:").pack(pady=5)
entry_descripcion = tk.Entry(root)
entry_descripcion.pack(pady=5)

tk.Label(root, text="Consola:").pack(pady=5)
entry_consola = tk.Entry(root)
entry_consola.pack(pady=5)

tk.Label(root, text="Año de Lanzamiento:").pack(pady=5)
entry_ano_lanzamiento = tk.Entry(root)
entry_ano_lanzamiento.pack(pady=5)

tk.Label(root, text="Número de Jugadores:").pack(pady=5)
entry_num_jugadores = tk.Entry(root)
entry_num_jugadores.pack(pady=5)

# Mostrar imagen actual o seleccionada
label_imagen = tk.Label(root)
label_imagen.pack(pady=10)

# Botón para seleccionar una nueva imagen
tk.Button(root, text="Seleccionar Imagen", command=seleccionar_imagen).pack(pady=10)

# Botón para actualizar los datos
tk.Button(root, text="Actualizar", command=actualizar_datos).pack(pady=20)

# Iniciar la interfaz
root.mainloop()

