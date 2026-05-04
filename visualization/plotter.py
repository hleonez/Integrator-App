import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import warnings

def plot_integral_window(parent, f, a, b, expression_str):
    """
    Crea una nueva ventana TopLevel que muestra el gráfico de matplotlib de f(x)
    y resalta el área entre x=a y x=b.
    Usa un tema oscuro para coincidir con CustomTkinter.
    """
    warnings.filterwarnings("ignore")
    
    # Crear una nueva ventana top level
    window = ctk.CTkToplevel(parent)
    window.title(f"Gráfica: {expression_str}")
    window.geometry("700x550")
    
    # Enfocar la ventana
    window.attributes("-topmost", True)
    window.after(500, lambda: window.attributes("-topmost", False))
    window.focus()

    # Configuración del tema oscuro de Matplotlib
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='#242424') # Coincide ligeramente con el tema oscuro de CTk
    ax.set_facecolor('#1E1E1E')
    
    # Generar datos
    margin = (b - a) * 0.2 if b > a else 1.0
    x_vals = np.linspace(a - margin, b + margin, 500)
    
    # Evaluar f(x)
    y_vals = np.array([f(val) for val in x_vals])
    
    # Dibujar la curva
    ax.plot(x_vals, y_vals, color='#4A9FE8', linewidth=2.5, label=f'f(x) = {expression_str}')
    
    # Rellenar el área bajo la curva
    x_fill = np.linspace(a, b, 300)
    y_fill = np.array([f(val) for val in x_fill])
    
    ax.fill_between(x_fill, 0, y_fill, color='#3B8ED5', alpha=0.35, label='Área a integrar')

    # Agregar ejes de origen
    ax.axhline(0, color='gray', linewidth=1)
    ax.axvline(0, color='gray', linewidth=1)
    
    # Marcar los límites a y b
    y_min, y_max = ax.get_ylim()
    ax.vlines(a, ymin=min(0, y_min), ymax=max(0, y_max), color='#F87171', linestyle='--', alpha=0.8, linewidth=1.5, label=f'a = {a}')
    ax.vlines(b, ymin=min(0, y_min), ymax=max(0, y_max), color='#4ADE80', linestyle='--', alpha=0.8, linewidth=1.5, label=f'b = {b}')
    
    # Título y etiquetas
    ax.set_title("Área bajo la curva", color='white', pad=15, fontsize=14, fontweight='bold')
    ax.set_xlabel('x', color='lightgray', fontsize=12)
    ax.set_ylabel('f(x)', color='lightgray', fontsize=12)
    
    # Leyenda y cuadrícula
    ax.legend(facecolor='#2B2B2B', edgecolor='gray', labelcolor='white')
    ax.grid(True, linestyle=':', color='gray', alpha=0.4)

    fig.tight_layout()

    # Incrustar en CTk
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True, padx=15, pady=15)
    
    def on_close():
        plt.close(fig)
        window.destroy()
        
    window.protocol("WM_DELETE_WINDOW", on_close)
