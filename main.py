import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import serial.tools.list_ports
import threading
import time
import pygame

# Inicializar Pygame Mixer
pygame.mixer.init()

# Datos de usuario para la simulación de autenticación
USUARIOS = {'admin': 'admin123'}

# Funciones de utilidad
def leer_datos_sensor(archivo='datos_sensor.txt'):
    datos = pd.read_csv(archivo, delimiter=',')  # Ajusta el delimitador según sea necesario
    return datos

def actualizar_grafico(datos):
    ax.clear()
    ax.plot(datos['Tiempo'], datos['Temperatura'], label='Temperatura')
    ax.plot(datos['Tiempo'], datos['Humedad'], label='Humedad')
    ax.plot(datos['Tiempo'], datos['Presion'], label='Presion')
    ax.legend()
    canvas.draw()
    verificar_temperatura(datos)

def reproducir_sonido(archivo_sonido):
    pygame.mixer.music.load(archivo_sonido)
    pygame.mixer.music.play(-1)  # -1 hace que la música se repita indefinidamente

def detener_sonido():
    pygame.mixer.music.stop()



# Modificación de la función verificar_temperatura
def verificar_temperatura(datos):
    if datos['Temperatura'].max() >= 50:
        reproducir_sonido("alarma.mp3")  # Inicia la alarma
        messagebox.showwarning("Alerta de temperatura", "Temperatura superior a 50 grados. Revisar sistemas.")
        detener_sonido()  # Detiene la alarma cuando el usuario cierra la ventana de alerta

def mostrar_principal():
    login_window.destroy()
    main_window.deiconify()

def verificar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if USUARIOS.get(usuario) == contraseña:
        mostrar_principal()
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrecta")

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de datos", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if archivo:
        datos = leer_datos_sensor(archivo)
        actualizar_grafico(datos)

def obtener_puertos_disponibles():
    puertos = serial.tools.list_ports.comports()
    return [puerto.device for puerto in puertos]

def conectar_puerto():
    puerto_seleccionado = combo_puertos.get()
    try:
        # Intenta abrir el puerto serial seleccionado
        ser = serial.Serial(puerto_seleccionado, 9600, timeout=1)
        messagebox.showinfo("Conexión de Puerto", f"Conectado al puerto {puerto_seleccionado}.")
        ser.close()
    except serial.SerialException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo abrir el puerto {puerto_seleccionado}.\n{e}")

def actualizar_puertos_disponibles():
    while True:
        # Obtiene la lista actual de puertos
        puertos_actuales = set(obtener_puertos_disponibles())
        puertos_en_combobox = set(combo_puertos['values'])

        # Si hay un cambio en los puertos disponibles, actualiza el ComboBox
        if puertos_actuales != puertos_en_combobox:
            def actualizar_combobox():
                combo_puertos['values'] = list(puertos_actuales)
                if combo_puertos.get() not in puertos_actuales:
                    combo_puertos.set('Seleccionar puerto')

            # Programa la actualización para que se ejecute en el hilo principal
            main_window.after(0, actualizar_combobox)

        # Espera un poco antes de revisar nuevamente
        time.sleep(0.1)

# Configuración inicial de Tkinter para la ventana principal
main_window = tk.Tk()
main_window.title("Monitor de Sensores")
main_window.withdraw()  # Oculta la ventana principal hasta que se haga login

# Configuración de la ventana de login
login_window = tk.Toplevel()
login_window.title("Login")
login_frame = tk.Frame(login_window)
login_frame.pack(padx=10, pady=10)

tk.Label(login_frame, text="Usuario:").grid(row=0, column=0)
entry_usuario = tk.Entry(login_frame)
entry_usuario.grid(row=0, column=1)

tk.Label(login_frame, text="Contraseña:").grid(row=1, column=0)
entry_contraseña = tk.Entry(login_frame, show="*")
entry_contraseña.grid(row=1, column=1)

boton_login = tk.Button(login_frame, text="Ingresar", command=verificar_login)
boton_login.grid(row=2, column=1)

# Elementos GUI de la ventana principal
frame = tk.Frame(main_window)
frame.pack()

boton_inicio = tk.Button(frame, text="Iniciar Monitoreo", command=lambda: actualizar_grafico(leer_datos_sensor()))
boton_inicio.pack(side=tk.LEFT)

boton_seleccionar = tk.Button(frame, text="Seleccionar otro archivo", command=seleccionar_archivo)
boton_seleccionar.pack(side=tk.LEFT)

# ComboBox para la selección del puerto COM
label_puerto = tk.Label(frame, text="Puerto COM:")
label_puerto.pack(side=tk.LEFT)
combo_puertos = ttk.Combobox(frame, values=obtener_puertos_disponibles(), state="readonly")
combo_puertos.pack(side=tk.LEFT)
combo_puertos.set('Seleccionar puerto')  # Mensaje por defecto

boton_conectar = tk.Button(frame, text="Conectar", command=conectar_puerto)
boton_conectar.pack(side=tk.LEFT)

boton_cerrar = tk.Button(frame, text="Cerrar", command=main_window.quit)
boton_cerrar.pack(side=tk.LEFT)

# Configuración de Matplotlib
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=main_window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Iniciar el hilo de fondo para actualizar los puertos disponibles
threading.Thread(target=actualizar_puertos_disponibles, daemon=True).start()

# Loop principal de la interfaz
main_window.mainloop()

# Integrantes
# - Josías Hidalgo Umaña
# - Franklin Castro Rodríguez
# - Diego Huertas González
# - María Graciela Mendez Rojas
# - Thomas Bermúdez Mora

# Conclusiones
# 1. Gestión eficiente de datos y alertas: La aplicación logró simular adecuadamente la gestión eficiente de los datos provenientes de los sensores, leyéndolos desde archivos de texto y permitiendo la generación de gráficos. La capacidad de activar una alarma sonora en caso de una temperatura superior a 50 grados garantiza una respuesta rápida ante situaciones críticas, mejorando la eficacia del monitoreo en tiempo real.
# 2. Flexibilidad y adaptabilidad del diseño: El proyecto demostró flexibilidad y adaptabilidad al incorporar todas las funcionalidades requeridas en una interfaz completa, dividida en una pantalla con todo el manejo del login y una pantalla dedicada a la lectura de información. Garantizando una experiencia de usuario cohesiva y fácil de usar, a pesar de la complejidad de las funciones implementadas.
# 3. Lectura de puerto COM: Se logró implementar la visualización del puerto COM, el cual está directamente vinculado con los puertos COM activos de la computadora. Esta funcionalidad fue validada físicamente mediante el uso de una placa CircuitPlayground, demostrando la efectividad y la precisión del sistema en tiempo real.