"""Main view - Empty placeholder for the application."""
import customtkinter as ctk
from ui.base_view import BaseView


class MainView(BaseView):
    """Main application view - starts empty."""
    
    def __init__(self):
        super().__init__()
        
        # Placeholder label
        self.placeholder_label = ctk.CTkLabel(
            self,
            text="Main Application\n(Coming Soon)",
            font=ctk.CTkFont(size=24, weight="normal", family="Segoe UI")
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")