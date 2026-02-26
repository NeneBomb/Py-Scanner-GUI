# 🛡️ Py-Scanner-GUI

Una interfaz gráfica (GUI) para **Nmap** desarrollada en Python utilizando la librería `tkinter`. Este proyecto permite realizar escaneos de red de forma visual sin necesidad de recordar todos los flags de la línea de comandos.

## ✨ Características
- **Interfaz Intuitiva:** Campos dedicados para IP/Rango y puertos.
- **Opciones de Escaneo:** Checkboxes para los modos más comunes (`-sV`, `-sC`, `-O`, `-A`, `-Pn`).
- **Output en Tiempo Real:** Consola integrada para ver el progreso del escaneo.
- **Lógica de Flags:** Construcción dinámica de comandos Nmap según la selección del usuario.

## 🚀 Requisitos
- Python 3.x
- Nmap instalado en el sistema.
- Tkinter.

## 🛠️ Uso
```bash
python3 scanner_gui.py
