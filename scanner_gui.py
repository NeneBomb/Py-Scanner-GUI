#!/bin/python3

import tkinter as tk
from tkinter import ttk
import subprocess

# --- Definición de las banderas de Nmap (Reestructurado) ---
# Usamos un diccionario de diccionarios para agrupar opciones excluyentes
OPCIONES_NMAP = {
    "Tipo de Escaneo": {
        "variable_name": "scan_type_var",
        "flags": [
            ("-sS", "SYN Stealth Scan (por defecto)"),
            ("-sT", "Connect Scan (Más ruidoso)"),
            ("-sU", "UDP Scan"),
            ("-sA", "ACK Scan (Firewall/Reglas)"),
            ("-sN", "Null Scan (Furtivo)"),
        ],
    },
    "Detección": {
        "variable_name": "detection_var",
        "flags": [
            ("", "Ninguna"), # Opción para no seleccionar nada
            ("-sV", "Detección de Versiones de Servicios"),
            ("-O", "Detección del Sistema Operativo (OS)"),
        ],
    },
    "Timing (Velocidad)": {
        "variable_name": "timing_var",
        "flags": [
            ("", "Normal"),
            ("-T0", "Paranoico (Más lento)"),
            ("-T3", "Normal (Por defecto)"),
            ("-T4", "Agresivo (Rápido)"),
            ("-T5", "Insane (Muy rápido, Inestable)"),
        ],
    },
}

# --- Variables Globales de Control ---
puertos_var = None
entrada_puertos = None
control_vars = {} 
checkbox_flags = {}

# --- Funciones Auxiliares ---

def crear_radio_flags(parent_frame, categoria_key):
    global control_vars

    var = tk.StringVar(value="")
    control_vars[categoria_key] = var
    
    opciones = OPCIONES_NMAP[categoria_key]
    
    for i, (flag_cmd, descripcion) in enumerate(opciones["flags"]):
        tk.Radiobutton(
            parent_frame, 
            text=f"{flag_cmd}: {descripcion}", 
            variable=var, 
            value=flag_cmd 
        ).pack(anchor='w', padx=10, pady=2)

def crear_checkbox_flag(parent_frame, flag_cmd, descripcion):
    global checkbox_flags
    var = tk.IntVar()
    
    chk = tk.Checkbutton(
        parent_frame,
        text=f"{flag_cmd}: {descripcion}",
        variable=var
    )
    chk.pack(anchor='w', padx=10, pady=2)
    checkbox_flags[flag_cmd] = var


# --- Función Principal para Ejecutar Nmap ---
def ejecutar_nmap():
    # 1. Obtener IP
    ip_objetivo = entrada_ip.get().strip()
    if not ip_objetivo:
        mostrar_resultado_en_gui("Error: Debes ingresar una IP o Hostname.", is_error=True)
        return

    comando_nmap = ["nmap"]
    
    for categoria in control_vars.values():
        flag = categoria.get()
        if flag:
            comando_nmap.append(flag)
    
    puertos_flag = puertos_var.get()
    if puertos_flag == "-p":
        rango = entrada_puertos.get().strip()
        if not rango:
            mostrar_resultado_en_gui("Error: La opción -p requiere un rango de puertos.", is_error=True)
            return
        comando_nmap.extend(["-p", rango])
    elif puertos_flag:
        comando_nmap.append(puertos_flag)

    for flag, var in checkbox_flags.items():
        if var.get() == 1:
            comando_nmap.append(flag)
    
    comando_nmap.append(ip_objetivo)
    
    # ... (Resto de la función de ejecución, misma lógica de subprocess.run)
    # ----------------------------------------------------------------------
    
    comando_str = " ".join(comando_nmap)
    print(f"Comando a ejecutar: {comando_str}")

    try:
        mostrar_resultado_en_gui(f"Ejecutando: {comando_str}\n\nEspere, Nmap puede tardar...", is_running=True)
        
        resultado = subprocess.run(
            comando_nmap,
            capture_output=True,
            text=True,
            check=True
        )
        
        salida = f"--- Ejecución Exitosa ---\n{resultado.stdout}"
        mostrar_resultado_en_gui(salida)
        
    except subprocess.CalledProcessError as e:
        salida_error = f"--- ERROR DE NMAP ---\nCódigo de error: {e.returncode}\n\n{e.stderr}"
        mostrar_resultado_en_gui(salida_error, is_error=True)
    except FileNotFoundError:
        mostrar_resultado_en_gui("Error: Nmap no está instalado o no se encuentra en el PATH.", is_error=True)


# --- Función Auxiliar para Mostrar Resultados en GUI (Sin cambios) ---
def mostrar_resultado_en_gui(texto_salida, is_error=False, is_running=False):
    area_texto.config(state=tk.NORMAL)
    area_texto.delete(1.0, tk.END) 
    
    color = "red" if is_error else ("gray" if is_running else "black")
    
    area_texto.insert(tk.END, texto_salida, color)
    area_texto.tag_config("red", foreground="red")
    area_texto.tag_config("gray", foreground="gray")
    
    area_texto.config(state=tk.DISABLED)
    notebook.select(pestaña_resultados)


# --- Configuración de la Ventana Principal ---
ventana = tk.Tk()
ventana.title("Mi propio Zenmap (GUI Nmap) - Radio Edition")
ventana.geometry("750x650")

# 1. Notebook y Pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(pady=10, padx=10, fill="both", expand=True)

# --- PEPESTAÑA 1: CONFIGURACIÓN ---
pestaña_config = ttk.Frame(notebook)
notebook.add(pestaña_config, text=" ⚙️ Configuración ")

# Marco para la IP
marco_ip = tk.LabelFrame(pestaña_config, text="IP/Host Objetivo", padx=5, pady=5)
marco_ip.pack(fill="x", padx=10, pady=10)
tk.Label(marco_ip, text="Introduce la IP/Dominio:").pack(side="left", padx=5)
entrada_ip = tk.Entry(marco_ip, width=40)
entrada_ip.pack(side="left", fill="x", expand=True, padx=5)

# 2. Marco principal de banderas
marco_flags = tk.LabelFrame(pestaña_config, text="Opciones de Escaneo", padx=10, pady=10)
marco_flags.pack(fill="both", expand=True, padx=10, pady=10)

# --- Submarcos para Radio Buttons (Excluyentes) ---
row_num = 0

# A. Tipo de Escaneo
marco_tipo_escaneo = tk.LabelFrame(marco_flags, text="Tipo de Escaneo (Elige 1)", padx=5, pady=5)
marco_tipo_escaneo.grid(row=row_num, column=0, sticky="nsew", padx=10, pady=5)
crear_radio_flags(marco_tipo_escaneo, "Tipo de Escaneo")

# B. Detección
marco_deteccion = tk.LabelFrame(marco_flags, text="Detección de Servicios/OS", padx=5, pady=5)
marco_deteccion.grid(row=row_num, column=1, sticky="nsew", padx=10, pady=5)
crear_radio_flags(marco_deteccion, "Detección")

# C. Timing
marco_timing = tk.LabelFrame(marco_flags, text="Velocidad (-T0 a -T5)", padx=5, pady=5)
marco_timing.grid(row=row_num, column=2, sticky="nsew", padx=10, pady=5)
crear_radio_flags(marco_timing, "Timing (Velocidad)")

row_num += 1

# --- Opción de Puertos (Con entrada de texto condicional) ---
marco_puertos = tk.LabelFrame(marco_flags, text="Selección de Puertos", padx=5, pady=5)
marco_puertos.grid(row=row_num, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

puertos_var = tk.StringVar(value="")

def toggle_puertos_entry():
    # Muestra o esconde el campo de entrada basado en la selección
    if puertos_var.get() == "-p":
        entrada_puertos.config(state=tk.NORMAL)
    else:
        entrada_puertos.delete(0, tk.END)
        entrada_puertos.config(state=tk.DISABLED)

tk.Radiobutton(marco_puertos, text="Puertos comunes (-F)", variable=puertos_var, value="-F", command=toggle_puertos_entry).pack(anchor='w', padx=10)
tk.Radiobutton(marco_puertos, text="Todos los puertos (-p-)", variable=puertos_var, value="-p-", command=toggle_puertos_entry).pack(anchor='w', padx=10)
tk.Radiobutton(marco_puertos, text="Rango específico (-p)", variable=puertos_var, value="-p", command=toggle_puertos_entry).pack(anchor='w', padx=10)

tk.Label(marco_puertos, text="Ej: 1-1024,80,443").pack(anchor='w', padx=30)
entrada_puertos = tk.Entry(marco_puertos, width=40)
entrada_puertos.pack(anchor='w', padx=30, pady=5)
entrada_puertos.config(state=tk.DISABLED) # Inicialmente deshabilitado

marco_simples = tk.LabelFrame(marco_flags, text="Opciones Adicionales", padx=5, pady=5)
marco_simples.grid(row=row_num, column=2, sticky="nsew", padx=10, pady=10)
crear_checkbox_flag(marco_simples, "--script=default", "Ejecutar scripts por defecto (Intrusivo)")
crear_checkbox_flag(marco_simples, "--open", "Mostrar solo puertos 'open' o 'open|filtered'")

boton_ejecutar = tk.Button(ventana, text=" ¡Escanear ahora!", 
                           command=ejecutar_nmap, bg="#008080", fg="white", font=("Arial", 14, "bold"))
boton_ejecutar.pack(pady=10, fill="x", padx=10)


# --- PEPESTAÑA 2: RESULTADOS (Sin cambios) ---
pestaña_resultados = ttk.Frame(notebook)
notebook.add(pestaña_resultados, text="  Resultados ")

area_texto = tk.Text(pestaña_resultados, wrap="word", width=60, height=15)
area_texto.pack(pady=10, padx=10, fill="both", expand=True)
area_texto.insert(tk.END, "El resultado de Nmap aparecerá aquí...")
area_texto.config(state=tk.DISABLED)

# Iniciar el bucle principal
ventana.mainloop()
