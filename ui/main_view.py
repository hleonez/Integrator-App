"""Main view - Main application view with math input and keyboard."""
import customtkinter as ctk
from ui.base_view import BaseView


class MainView(BaseView):
    """Main application view with math input field and virtual keyboard."""
    
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
        
        # Send button (calculate)
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
        
        # Placeholder content area
        self.placeholder_label = ctk.CTkLabel(
            self,
            text="Main Application\n(Coming Soon)",
            font=ctk.CTkFont(size=24, weight="normal", family="Segoe UI")
        )
        self.placeholder_label.place(relx=0.5, rely=0.6, anchor="center")
    
    def open_keyboard(self):
        """Open the virtual math keyboard."""
        from ui.keyboard_view import KeyboardView
        keyboard = KeyboardView(parent=self, input_widget=self.math_input)
    
    def send_function(self):
        """Placeholder for sending function to core for calculation."""
        # TODO: Implement function parsing and calculation
        function_text = self.math_input.get("0.0", "end").strip()
        if function_text:
            print(f"Función a procesar: {function_text}")