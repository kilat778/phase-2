import psycopg2
import tkinter as tk
from tkinter import messagebox

# Función para borrar el juego de la base de datos
def borrar_juego():
    id_juego = entry_id.get()

    if not id_juego:
        messagebox.showerror("Error", "Debe ingresar el ID del juego a eliminar.")
        return

    # Confirmación antes de borrar
    respuesta = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar el juego con ID {id_juego}?")
    
    if respuesta:
        try:
            # Conectar a la base de datos
            conn = psycopg2.connect("dbname=test1 user=postgres password=123456 host=localhost")
            cur = conn.cursor()

            # Borrar el juego por ID
            cur.execute("DELETE FROM juegos WHERE Codigo = %s;", (id_juego,))
            conn.commit()

            # Verificar si se borró un registro
            if cur.rowcount > 0:
                messagebox.showinfo("Éxito", f"El juego con ID {id_juego} ha sido eliminado.")
            else:
                messagebox.showinfo("Información", f"No se encontró ningún juego con el ID {id_juego}.")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al borrar el juego: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Eliminar Juego")
root.geometry("400x200")

# Etiqueta y campo de entrada para el ID del juego
tk.Label(root, text="Ingrese el ID del Juego a eliminar:").pack(pady=10)
entry_id = tk.Entry(root)
entry_id.pack(pady=10)

# Botón para borrar el juego
tk.Button(root, text="Eliminar Juego", command=borrar_juego, bg="red", fg="white").pack(pady=20)

# Iniciar la interfaz
root.mainloop()
