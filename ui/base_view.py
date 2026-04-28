"""Base view module for UI components."""
import customtkinter as ctk


class BaseView(ctk.CTk):
    """Base view class with theme toggle functionality."""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Integrator App")
        self.geometry("800x600")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create theme toggle button (top right)
        self.theme_button = ctk.CTkButton(
            self,
            text="🌙",
            width=40,
            height=30,
            command=self.toggle_theme,
            fg_color="transparent",
            border_width=0,
            hover=True
        )
        self.theme_button.grid(row=0, column=0, sticky="ne", padx=10, pady=10)
        
        # Set initial theme
        self.current_theme = "dark"
        ctk.set_appearance_mode("dark")
    
    def toggle_theme(self):
        """Toggle between light and dark mode."""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_button.configure(text="☀️")
            ctk.set_appearance_mode("light")
        else:
            self.current_theme = "dark"
            self.theme_button.configure(text="🌙")
            ctk.set_appearance_mode("dark")