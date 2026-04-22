# ️ Py-Scanner-GUI

Una interfaz gráfica (GUI) profesional para **Nmap** desarrollada en Python utilizando la librería `tkinter`. Este proyecto permite realizar auditorías de red de forma visual, facilitando la construcción de comandos complejos de Nmap mediante una interfaz intuitiva.

---

##  Características / Features:
- **Interfaz Intuitiva / Intuitive UI:** Campos dedicados para IP/Rango y selección de puertos.
- **Modos de Escaneo / Scan Modes:** Checkboxes para activar funciones avanzadas (`-sV`, `-sC`, `-O`, `-A`, `-Pn`).
- **Consola Integrada / Live Output:** Visualización en tiempo real de la salida de Nmap dentro de la aplicación.
- **Multihilo / Threading:** La interfaz no se bloquea mientras el escaneo está en curso.

##  Uso / Usage

###  Instrucciones:
1. **Requisitos:** Tener instalado Python 3 y Nmap en el sistema.
2. **Ejecución:** Corre el script con `python3 scanner_gui.py`.
3. **Escaneo:** Introduce la IP objetivo, selecciona los flags deseados y pulsa "Escanear".

###  Instructions:
1. **Requirements:** Python 3 and Nmap must be installed on your system.
2. **Execution:** Run the script using `python3 scanner_gui.py`.
3. **Scanning:** Enter the target IP, select your preferred scan flags, and click "Escanear".

---

## ️ Requisitos Técnicos / Technical Requirements
- Python 3.x
- Nmap (Binary must be in system PATH)
- Tkinter (Standard Python library)

## ⚠️ Disclaimer / Aviso Legal
Este proyecto fue desarrollado exclusivamente con fines educativos y de seguridad ética. El autor no se hace responsable del mal uso de esta herramienta.

This project was developed for educational and ethical security purposes only. The author is not responsible for any misuse of this tool.
