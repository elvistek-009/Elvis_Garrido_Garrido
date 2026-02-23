import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ---------------- CONEXIÓN A LA BASE DE DATOS ----------------
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="Benja009",       
        database="agencia_autos"
    )

# ---------------- FUNCIONES CRUD ----------------
def agregar_vehiculo():
    marca = entry_marca.get()
    modelo = entry_modelo.get()
    anio = entry_anio.get()
    combustible = entry_combustible.get()

    if marca == "" or modelo == "":
        messagebox.showwarning("Validación", "Marca y modelo son obligatorios")
        return

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO vehiculos (marca, modelo, año, combustible)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (marca, modelo, anio, combustible))
        conexion.commit()
        conexion.close()
        limpiar_campos()
        mostrar_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo agregado correctamente")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mostrar_vehiculos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM vehiculos")
    registros = cursor.fetchall()
    conexion.close()

    for fila in registros:
        estado = "Disponible" if fila[5] else "No disponible"
        tabla.insert("", tk.END, values=(fila[0], fila[1], fila[2], fila[3], fila[4], estado))

def actualizar_estado():
    seleccionado = tabla.focus()
    if seleccionado == "":
        messagebox.showwarning("Selección", "Seleccione un vehículo")
        return

    valores = tabla.item(seleccionado, "values")
    id_vehiculo = valores[0]
    nuevo_estado = False if valores[5] == "Disponible" else True

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE vehiculos SET disponible=%s WHERE id=%s",
        (nuevo_estado, id_vehiculo)
    )
    conexion.commit()
    conexion.close()
    mostrar_vehiculos()

def limpiar_campos():
    entry_marca.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_anio.delete(0, tk.END)
    entry_combustible.delete(0, tk.END)

# ---------------- INTERFAZ GRÁFICA ----------------
ventana = tk.Tk()
ventana.title("Agencia de Alquiler de Vehículos")
ventana.geometry("800x500")

# -------- FORMULARIO --------
frame_form = tk.LabelFrame(ventana, text="Registro de Vehículos")
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Marca").grid(row=0, column=0, padx=5, pady=5)
entry_marca = tk.Entry(frame_form)
entry_marca.grid(row=0, column=1)

tk.Label(frame_form, text="Modelo").grid(row=0, column=2, padx=5, pady=5)
entry_modelo = tk.Entry(frame_form)
entry_modelo.grid(row=0, column=3)

tk.Label(frame_form, text="Año").grid(row=1, column=0, padx=5, pady=5)
entry_anio = tk.Entry(frame_form)
entry_anio.grid(row=1, column=1)

tk.Label(frame_form, text="Combustible").grid(row=1, column=2, padx=5, pady=5)
entry_combustible = tk.Entry(frame_form)
entry_combustible.grid(row=1, column=3)

btn_agregar = tk.Button(frame_form, text="Agregar Vehículo", command=agregar_vehiculo)
btn_agregar.grid(row=2, column=0, columnspan=4, pady=10)

# -------- TABLA --------
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

columnas = ("ID", "Marca", "Modelo", "Año", "Combustible", "Estado")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=120)

tabla.pack(fill="both", expand=True)

# -------- BOTONES --------
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

btn_actualizar = tk.Button(frame_botones, text="Cambiar Disponibilidad", command=actualizar_estado)
btn_actualizar.pack()

# Cargar datos iniciales
mostrar_vehiculos()

ventana.mainloop()
