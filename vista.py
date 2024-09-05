import tkinter as tk
import os

# Funciones para abrir los scripts
def abrir_actualizar():
    os.system('python actualizar.py')

def abrir_borrar():
    os.system('python borrar.py')

def abrir_insertar():
    os.system('python insertar.py')

def abrir_leer():
    os.system('python leer.py')

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Juegos")
root.geometry("300x300")

# Etiqueta del título
tk.Label(root, text="Gestión de Juegos", font=("Helvetica", 16)).pack(pady=20)

# Botón para abrir la interfaz de actualizar
tk.Button(root, text="Actualizar Juego", command=abrir_actualizar, width=20).pack(pady=10)

# Botón para abrir la interfaz de borrar
tk.Button(root, text="Borrar Juego", command=abrir_borrar, width=20).pack(pady=10)

# Botón para abrir la interfaz de insertar
tk.Button(root, text="Insertar Juego", command=abrir_insertar, width=20).pack(pady=10)

# Botón para abrir la interfaz de leer
tk.Button(root, text="Leer Juegos", command=abrir_leer, width=20).pack(pady=10)

# Iniciar la interfaz
root.mainloop()
