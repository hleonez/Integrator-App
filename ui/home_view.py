"""Vista principal - Menú principal de la aplicación."""
import customtkinter as ctk
from ui.base_view import BaseView


class HomeView(BaseView):
    """Vista principal con el título de la aplicación y navegación a la aplicación principal."""
    
    def __init__(self):
        super().__init__()
        
        # Etiqueta del título
        self.title_label = ctk.CTkLabel(
            self,
            text="Integrator App",
            font=ctk.CTkFont(size=48, weight="bold", family="Segoe UI")
        )
        self.title_label.place(relx=0.5, rely=0.42, anchor="center")
        
        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Tu centro de integración",
            font=ctk.CTkFont(size=18, weight="normal", family="Segoe UI")
        )
        self.subtitle_label.place(relx=0.5, rely=0.53, anchor="center")
        
        # Botón de inicio
        self.start_button = ctk.CTkButton(
            self,
            text="Comenzar",
            width=200,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("#3B8ED5", "#1F6AA5"),
            hover_color=("#4A9FE8", "#2A7AB5"),
            command=self.go_to_main_view
        )
        self.start_button.place(relx=0.5, rely=0.65, anchor="center")
    
    def go_to_main_view(self):
        """Navegar a la vista principal de la aplicación."""
        from ui.main_view import MainView
        self.go_to_view(MainView)