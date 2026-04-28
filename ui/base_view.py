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
        
        # Set initial theme
        self.current_theme = "dark"
        ctk.set_appearance_mode("dark")
        
        # Create theme toggle button (top right) - rounded and visible
        self.theme_button = ctk.CTkButton(
            self,
            text="🌙",
            width=45,
            height=35,
            corner_radius=20,
            command=self.toggle_theme,
            fg_color=("#3B8ED5", "#1F6AA5"),  # Blue for dark mode
            hover_color=("#4A9FE8", "#2A7AB5"),
            border_width=0,
        )
        self.theme_button.grid(row=0, column=0, sticky="ne", padx=15, pady=15)
    
    def toggle_theme(self):
        """Toggle between light and dark mode."""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_button.configure(
                text="☀️",
                fg_color=("#6B7280", "#4B5563"),  # Gray for light mode
                hover_color=("#7B8290", "#5B6573")
            )
            ctk.set_appearance_mode("light")
        else:
            self.current_theme = "dark"
            self.theme_button.configure(
                text="🌙",
                fg_color=("#3B8ED5", "#1F6AA5"),
                hover_color=("#4A9FE8", "#2A7AB5")
            )
            ctk.set_appearance_mode("dark")
    
    def go_to_view(self, view_class):
        """Navigate to another view."""
        self.withdraw()
        new_window = view_class()
        new_window.mainloop()
        self.destroy()