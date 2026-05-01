import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import warnings

def plot_integral_window(parent, f, a, b, expression_str):
    """
    Creates a new TopLevel window displaying the matplotlib graph of f(x)
    and highlighting the area between x=a and x=b.
    Uses a dark theme to match CustomTkinter.
    """
    warnings.filterwarnings("ignore")
    
    # Create a new top level window
    window = ctk.CTkToplevel(parent)
    window.title(f"Gráfica: {expression_str}")
    window.geometry("700x550")
    
    # Focus window
    window.attributes("-topmost", True)
    window.after(500, lambda: window.attributes("-topmost", False))
    window.focus()

    # Matplotlib dark theme configuration
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='#242424') # Matches CTk dark theme slightly
    ax.set_facecolor('#1E1E1E')
    
    # Generate data
    margin = (b - a) * 0.2 if b > a else 1.0
    x_vals = np.linspace(a - margin, b + margin, 500)
    
    # Evaluate f(x)
    y_vals = np.array([f(val) for val in x_vals])
    
    # Plot curve
    ax.plot(x_vals, y_vals, color='#4A9FE8', linewidth=2.5, label=f'f(x) = {expression_str}')
    
    # Fill area under curve
    x_fill = np.linspace(a, b, 300)
    y_fill = np.array([f(val) for val in x_fill])
    
    ax.fill_between(x_fill, 0, y_fill, color='#3B8ED5', alpha=0.35, label='Área a integrar')

    # Add origin axes
    ax.axhline(0, color='gray', linewidth=1)
    ax.axvline(0, color='gray', linewidth=1)
    
    # Mark a and b limits
    y_min, y_max = ax.get_ylim()
    ax.vlines(a, ymin=min(0, y_min), ymax=max(0, y_max), color='#F87171', linestyle='--', alpha=0.8, linewidth=1.5, label=f'a = {a}')
    ax.vlines(b, ymin=min(0, y_min), ymax=max(0, y_max), color='#4ADE80', linestyle='--', alpha=0.8, linewidth=1.5, label=f'b = {b}')
    
    # Title and labels
    ax.set_title("Área bajo la curva", color='white', pad=15, fontsize=14, fontweight='bold')
    ax.set_xlabel('x', color='lightgray', fontsize=12)
    ax.set_ylabel('f(x)', color='lightgray', fontsize=12)
    
    # Legend and grid
    ax.legend(facecolor='#2B2B2B', edgecolor='gray', labelcolor='white')
    ax.grid(True, linestyle=':', color='gray', alpha=0.4)

    fig.tight_layout()

    # Embed in CTk
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True, padx=15, pady=15)
    
    def on_close():
        plt.close(fig)
        window.destroy()
        
    window.protocol("WM_DELETE_WINDOW", on_close)
