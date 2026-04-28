"""Home view - Main menu of the application."""
import customtkinter as ctk
from ui.base_view import BaseView


class HomeView(BaseView):
    """Home view with app title and navigation to main app."""
    
    def __init__(self):
        super().__init__()
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Integrator App",
            font=ctk.CTkFont(size=48, weight="bold", family="Segoe UI")
        )
        self.title_label.place(relx=0.5, rely=0.35, anchor="center")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Your integration hub",
            font=ctk.CTkFont(size=18, weight="normal", family="Segoe UI")
        )
        self.subtitle_label.place(relx=0.5, rely=0.45, anchor="center")
        
        # Start button - rounded with hover animation
        self.start_button = ctk.CTkButton(
            self,
            text="Start",
            width=200,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("#3B8ED5", "#1F6AA5"),
            hover_color=("#4A9FE8", "#2A7AB5"),
            command=self.go_to_main_view
        )
        self.start_button.place(relx=0.5, rely=0.6, anchor="center")
    
    def go_to_main_view(self):
        """Navigate to the main application view."""
        from ui.main_view import MainView
        self.go_to_view(MainView)