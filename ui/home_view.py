"""Home view - Main menu of the application."""
import customtkinter as ctk
from ui.base_view import BaseView


class HomeView(BaseView):
    """Home view with app title and navigation to main app."""
    
    def __init__(self):
        super().__init__()
        
        # Create input frame at top
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.place(relx=0.5, rely=0.12, anchor="center", relwidth=0.85)
        
        # Math input field (CTkTextbox for multi-line support)
        self.math_input = ctk.CTkTextbox(
            self.input_frame,
            height=45,
            font=ctk.CTkFont(size=18, family="Consolas"),
            wrap="none"
        )
        self.math_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Send button (calculate) - placeholder, no functionality yet
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="➤",
            width=50,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=20),
            fg_color=("#3B8ED5", "#1F6AA5"),
            hover_color=("#4A9FE8", "#2A7AB5"),
            command=self.send_function
        )
        self.send_button.pack(side="left")
        
        # Keyboard toggle button below input
        self.keyboard_toggle = ctk.CTkButton(
            self,
            text="⌨️ Teclado",
            width=150,
            height=40,
            corner_radius=15,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#6B4C9A", "#4B2C7A"),
            hover_color=("#7B5CAA", "#5B3C8A"),
            command=self.open_keyboard
        )
        self.keyboard_toggle.place(relx=0.5, rely=0.22, anchor="center")
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Integrator App",
            font=ctk.CTkFont(size=48, weight="bold", family="Segoe UI")
        )
        self.title_label.place(relx=0.5, rely=0.45, anchor="center")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Your integration hub",
            font=ctk.CTkFont(size=18, weight="normal", family="Segoe UI")
        )
        self.subtitle_label.place(relx=0.5, rely=0.55, anchor="center")
        
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
        self.start_button.place(relx=0.5, rely=0.72, anchor="center")
    
    def open_keyboard(self):
        """Open the virtual math keyboard."""
        from ui.keyboard_view import KeyboardView
        keyboard = KeyboardView(input_widget=self.math_input)
        keyboard.mainloop()
    
    def send_function(self):
        """Placeholder for sending function to core for calculation."""
        # TODO: Implement function parsing and calculation
        function_text = self.math_input.get("0.0", "end").strip()
        if function_text:
            print(f"Función a procesar: {function_text}")
            # Placeholder - button exists but doesn't do anything yet
    
    def go_to_main_view(self):
        """Navigate to the main application view."""
        from ui.main_view import MainView
        self.go_to_view(MainView)