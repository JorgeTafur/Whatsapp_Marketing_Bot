import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Definir rutas por defecto
ruta_por_defecto_excel = os.path.join(os.getcwd(), 'numbers.xlsx')
ruta_por_defecto_texto = os.path.join(os.getcwd(), 'message.txt')
ruta_por_defecto_imagenes = os.path.join(os.getcwd(), 'img')

def cargar_configuracion():
    if os.path.exists('config.txt'):
        with open('config.txt', 'r') as config_file:
            lineas = config_file.readlines()
            if len(lineas) == 3:
                return lineas[0].strip(), lineas[1].strip(), lineas[2].strip()
    return ruta_por_defecto_excel, ruta_por_defecto_texto, ruta_por_defecto_imagenes

def seleccionar_archivo_excel():
    archivo_excel = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx")])
    if archivo_excel:
        entrada_excel.delete(0, tk.END)
        entrada_excel.insert(0, archivo_excel)

def seleccionar_archivo_texto():
    archivo_texto = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo_texto:
        entrada_texto.delete(0, tk.END)
        entrada_texto.insert(0, archivo_texto)

def seleccionar_carpeta_imagenes():
    carpeta_imagenes = filedialog.askdirectory()
    if carpeta_imagenes:
        entrada_imagenes.delete(0, tk.END)
        entrada_imagenes.insert(0, carpeta_imagenes)

def verificar_rutas(ruta_excel, ruta_texto, ruta_imagenes):
    if not os.path.exists(ruta_excel):
        messagebox.showwarning("Advertencia", f"No se encontró el archivo de Excel especificado.\nUsando ruta por defecto: {ruta_por_defecto_excel}")
        ruta_excel = ruta_por_defecto_excel
    if not os.path.exists(ruta_texto):
        messagebox.showwarning("Advertencia", f"No se encontró el archivo de texto especificado.\nUsando ruta por defecto: {ruta_por_defecto_texto}")
        ruta_texto = ruta_por_defecto_texto
    if not os.path.exists(ruta_imagenes):
        messagebox.showwarning("Advertencia", f"No se encontró la carpeta de imágenes especificada.\nUsando ruta por defecto: {ruta_por_defecto_imagenes}")
        ruta_imagenes = ruta_por_defecto_imagenes
    return ruta_excel, ruta_texto, ruta_imagenes

def guardar_configuracion():
    ruta_excel = entrada_excel.get() or ruta_por_defecto_excel
    ruta_texto = entrada_texto.get() or ruta_por_defecto_texto
    ruta_imagenes = entrada_imagenes.get() or ruta_por_defecto_imagenes

    ruta_excel, ruta_texto, ruta_imagenes = verificar_rutas(ruta_excel, ruta_texto, ruta_imagenes)

    try:
        with open('config.txt', 'w') as config_file:
            config_file.write(f'{ruta_excel}\n')
            config_file.write(f'{ruta_texto}\n')
            config_file.write(f'{ruta_imagenes}\n')
        messagebox.showinfo("Éxito", "Configuración guardada con éxito.")
        ventana.destroy()  # Cerrar la ventana después de guardar la configuración
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la configuración: {e}")

# Cargar la configuración existente o usar los valores por defecto
ruta_excel, ruta_texto, ruta_imagenes = cargar_configuracion()

# Crear la ventana de configuración
ventana = tk.Tk()
ventana.title("Configuración de Envío de WhatsApp")

# Entrada y botón para seleccionar el archivo Excel
tk.Label(ventana, text="Archivo Excel de números:").grid(row=0, column=0, padx=10, pady=10)
entrada_excel = tk.Entry(ventana, width=50)
entrada_excel.insert(0, ruta_excel)
entrada_excel.grid(row=0, column=1, padx=10, pady=10)
tk.Button(ventana, text="Seleccionar", command=seleccionar_archivo_excel).grid(row=0, column=2, padx=10, pady=10)

# Entrada y botón para seleccionar el archivo de texto del mensaje
tk.Label(ventana, text="Archivo de texto del mensaje:").grid(row=1, column=0, padx=10, pady=10)
entrada_texto = tk.Entry(ventana, width=50)
entrada_texto.insert(0, ruta_texto)
entrada_texto.grid(row=1, column=1, padx=10, pady=10)
tk.Button(ventana, text="Seleccionar", command=seleccionar_archivo_texto).grid(row=1, column=2, padx=10, pady=10)

# Entrada y botón para seleccionar la carpeta de imágenes
tk.Label(ventana, text="Carpeta de imágenes:").grid(row=2, column=0, padx=10, pady=10)
entrada_imagenes = tk.Entry(ventana, width=50)
entrada_imagenes.insert(0, ruta_imagenes)
entrada_imagenes.grid(row=2, column=1, padx=10, pady=10)
tk.Button(ventana, text="Seleccionar", command=seleccionar_carpeta_imagenes).grid(row=2, column=2, padx=10, pady=10)

# Botón para guardar la configuración
tk.Button(ventana, text="Guardar Configuración", command=guardar_configuracion).grid(row=3, column=0, columnspan=3, pady=20)

ventana.mainloop()
