"""Keyboard view - Virtual mathematical keyboard for inputting functions."""
import customtkinter as ctk


class KeyboardView(ctk.CTkToplevel):
    """Virtual keyboard for mathematical functions.
    
    Uses CTkToplevel instead of inheriting BaseView so it behaves as a
    secondary floating window, avoiding geometry manager conflicts with
    the parent window's grid layout.
    """
    
    def __init__(self, parent=None, input_widget=None, callback=None):
        """Initialize keyboard view.
        
        Args:
            parent: The parent window (CTk instance)
            input_widget: The CTkTextbox or CTkEntry to insert text into
            callback: Optional callback function to call when text is inserted
        """
        super().__init__(parent)
        
        self.input_widget = input_widget
        self.callback = callback
        self.current_tab = "basic"
        
        # Configure window
        self.title("Math Keyboard")
        self.geometry("700x550")
        self.resizable(True, True)
        
        # Keep on top of parent
        self.transient(parent)
        self.lift()
        self.focus_force()
        
        # Create main container — pack is safe here, CTkToplevel has no pre-existing slaves
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tab buttons frame
        self.tab_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_frame.pack(fill="x", pady=(0, 10))
        
        # Create tab buttons
        self.tabs = {}
        tab_names = ["Basic", "Funciones", "Trig", "Constantes", "Avanzado"]
        tab_keys = ["basic", "funciones", "trig", "constantes", "avanzado"]
        
        for name, key in zip(tab_names, tab_keys):
            btn = ctk.CTkButton(
                self.tab_frame,
                text=name,
                width=100,
                height=35,
                corner_radius=15,
                fg_color=("#3B8ED5", "#1F6AA5") if key == "basic" else ("#4a4a4a", "#2d2d2d"),
                hover_color=("#5A9FE8", "#3A8AB5"),
                command=lambda k=key: self.switch_tab(k)
            )
            btn.pack(side="left", padx=5)
            self.tabs[key] = btn
        
        # Create keyboard buttons frame
        self.keyboard_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="",
            fg_color="transparent"
        )
        self.keyboard_frame.pack(fill="both", expand=True)
        
        # Show initial tab
        self.show_keyboard("basic")
    
    def switch_tab(self, tab_key):
        """Switch to a different keyboard tab."""
        for key, btn in self.tabs.items():
            if key == tab_key:
                btn.configure(fg_color=("#3B8ED5", "#1F6AA5"))
            else:
                btn.configure(fg_color=("#4a4a4a", "#2d2d2d"))
        
        self.current_tab = tab_key
        self.show_keyboard(tab_key)
    
    def show_keyboard(self, tab_key):
        """Show the keyboard for the specified tab."""
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        
        if tab_key == "basic":
            self.create_basic_keyboard()
        elif tab_key == "funciones":
            self.create_funciones_keyboard()
        elif tab_key == "trig":
            self.create_trig_keyboard()
        elif tab_key == "constantes":
            self.create_constantes_keyboard()
        elif tab_key == "avanzado":
            self.create_avanzado_keyboard()
    
    def insert_text(self, text):
        """Insert text into the input widget."""
        if self.input_widget:
            try:
                self.input_widget.insert("end", text)
            except Exception:
                self.input_widget.insert("end", text)
        
        if self.callback:
            self.callback(text)
    
    def create_button(self, parent, text, insert_text, width=60, height=40):
        """Create a keyboard button."""
        btn = ctk.CTkButton(
            parent,
            text=text,
            width=width,
            height=height,
            corner_radius=8,
            fg_color=("#3B3B3B", "#2d2d2d"),
            hover_color=("#4A4A4A", "#3d3d3d"),
            border_width=1,
            border_color=("#5A5A5A", "#4A4A4A"),
            command=lambda t=insert_text: self.insert_text(t)
        )
        return btn
    
    def create_basic_keyboard(self):
        """Create BASIC tab keyboard."""
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for num in numbers:
            btn = self.create_button(row, num, num, width=55, height=45)
            btn.pack(side="left", padx=2)
        
        operators = [("+", "+"), ("-", "-"), ("*", "*"), ("/", "/"), ("^", "**")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in operators:
            btn = self.create_button(row, text, insert, width=55, height=45)
            btn.pack(side="left", padx=2)
        
        grouping = [("(", "("), (")", ")"), (".", ".")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in grouping:
            btn = self.create_button(row, text, insert, width=55, height=45)
            btn.pack(side="left", padx=2)
        
        powers = [("x²", "**2"), ("x³", "**3"), ("xⁿ", "**"), ("√", "sqrt("), ("ⁿ√", "root(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in powers:
            btn = self.create_button(row, text, insert, width=80, height=45)
            btn.pack(side="left", padx=2)
        
        others = [("|x|", "abs("), ("1/x", "1/()"), ("=", "=")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in others:
            btn = self.create_button(row, text, insert, width=80, height=45)
            btn.pack(side="left", padx=2)
        
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        btn = self.create_button(row, "x", "x", width=80, height=45)
        btn.pack(side="left", padx=2)
        btn = self.create_button(row, "y", "y", width=80, height=45)
        btn.pack(side="left", padx=2)
    
    def create_funciones_keyboard(self):
        """Create FUNCIONES tab keyboard."""
        funcs1 = [("ln", "log("), ("log", "log10("), ("exp", "exp(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in funcs1:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        funcs2 = [("e^x", "exp("), ("log₂", "log2("), ("10^x", "10**")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in funcs2:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=10)
        btn = ctk.CTkButton(
            row,
            text="🗑️ Limpiar",
            width=150,
            height=45,
            corner_radius=10,
            fg_color=("#8B4444", "#6B3333"),
            hover_color=("#9B5454", "#7B4343"),
            command=self.clear_input
        )
        btn.pack(side="left", padx=3)
    
    def create_trig_keyboard(self):
        """Create TRIGONOMETRÍA tab keyboard."""
        trig1 = [("sin", "sin("), ("cos", "cos("), ("tan", "tan(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in trig1:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        trig2 = [("arcsin", "asin("), ("arccos", "acos("), ("arctan", "atan(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in trig2:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        trig3 = [("cot", "cot("), ("sec", "sec("), ("csc", "csc(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in trig3:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        hyper = [("sinh", "sinh("), ("cosh", "cosh("), ("tanh", "tanh(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in hyper:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
    
    def create_constantes_keyboard(self):
        """Create CONSTANTES tab keyboard."""
        const1 = [("π", "pi"), ("e", "E"), ("∞", "inf")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in const1:
            btn = self.create_button(row, text, insert, width=100, height=60)
            btn.pack(side="left", padx=3)
        
        const2 = [("i", "1j"), ("φ", "(1+sqrt(5))/2")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in const2:
            btn = self.create_button(row, text, insert, width=100, height=60)
            btn.pack(side="left", padx=3)
        
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=10)
        btn = self.create_button(row, "E (euler)", "E", width=150, height=50)
        btn.pack(side="left", padx=3)
    
    def create_avanzado_keyboard(self):
        """Create AVANZADO tab keyboard."""
        ops = [("Σ", "sum("), ("∏", "prod("), ("∫", "integrate(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in ops:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        btn = self.create_button(row, "lim", "limit(", width=150, height=50)
        btn.pack(side="left", padx=3)
        
        others = [("n!", "factorial("), ("floor", "floor("), ("ceil", "ceil(")]
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        for text, insert in others:
            btn = self.create_button(row, text, insert, width=100, height=50)
            btn.pack(side="left", padx=3)
        
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        btn = self.create_button(row, "d/dx", "diff(", width=150, height=50)
        btn.pack(side="left", padx=3)
        
        row = ctk.CTkFrame(self.keyboard_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        btn = self.create_button(row, "%", "%", width=80, height=50)
        btn.pack(side="left", padx=3)
    
    def clear_input(self):
        """Clear the input widget."""
        if self.input_widget:
            try:
                self.input_widget.delete("0.0", "end")
            except Exception:
                self.input_widget.delete(0, "end")