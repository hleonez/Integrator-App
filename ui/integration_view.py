"""Integration view - UI for numerical integration methods.

Provides a single view where the user can:
  - Type a mathematical function of x.
  - Set the integration interval [a, b] and number of subintervals n.
  - Choose between Riemann, Trapezoidal, Simpson, or Boole.
  - See the numerical result immediately.
"""

import math
import customtkinter as ctk
from sympy import sympify, lambdify, symbols, SympifyError

from ui.base_view import BaseView
from core.riemann import riemann
from core.trapezoidal import trapezoidal
from core.simpson import simpson
from core.boole import boole
from core.punto_medio import midpoint
from core.cuadratura_gauss import gauss_quadrature_2
from core.romberg import romberg
from visualization.plotter import plot_integral_window


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

METHODS = {
    "Riemann (Punto Medio)": {
        "function": riemann,
        "n_constraint": "cualquier entero ≥ 1",
        "n_default": "100",
    },
    "Regla Trapezoidal": {
        "function": trapezoidal,
        "n_constraint": "cualquier entero ≥ 1",
        "n_default": "100",
    },
    "Regla de Simpson 1/3": {
        "function": simpson,
        "n_constraint": "entero par ≥ 2",
        "n_default": "100",
    },
    "Regla de Boole": {
        "function": boole,
        "n_constraint": "múltiplo de 4 ≥ 4",
        "n_default": "100",
    },
    "Método de Punto Medio": {
        "function": midpoint,
        "n_constraint": "cualquier entero ≥ 1",
        "n_default": "100",
    },
    "Cuadratura de Gauss (2 puntos)": {
        "function": gauss_quadrature_2,
        "n_constraint": "no aplica",
        "n_default": "- - -",
    },
    "Método de Romberg": {
        "function": romberg,
        "n_constraint": "ITERACIONES ≥ 1",
        "n_default": "5",
    },
}

# Safe math symbols available when evaluating user-typed functions
SAFE_MATH_NAMESPACE = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}


# ---------------------------------------------------------------------------
# View
# ---------------------------------------------------------------------------

class IntegrationView(BaseView):
    """View for computing definite integrals with selectable numerical methods."""

    def __init__(self):
        super().__init__()
        self.title("Integrator App – Métodos de Integración")
        self.geometry("820x680")

        self._build_header()
        self._build_method_selector()
        self._build_inputs()
        self._build_action_buttons()
        self._build_result_panel()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------

    def _build_header(self) -> None:
        """Title and subtitle at the top of the view."""
        self.header_label = ctk.CTkLabel(
            self,
            text="Integración Numérica",
            font=ctk.CTkFont(size=32, weight="bold", family="Segoe UI"),
        )
        self.header_label.place(relx=0.5, rely=0.07, anchor="center")

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Área bajo la curva",
            font=ctk.CTkFont(size=15, family="Segoe UI"),
            text_color=("gray40", "gray70"),
        )
        self.subtitle_label.place(relx=0.5, rely=0.13, anchor="center")

    def _build_method_selector(self) -> None:
        """Dropdown to choose the integration method."""
        self.method_label = ctk.CTkLabel(
            self,
            text="Método:",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.method_label.place(relx=0.08, rely=0.21, anchor="w")

        self.method_var = ctk.StringVar(value=list(METHODS.keys())[0])
        self.method_dropdown = ctk.CTkOptionMenu(
            self,
            values=list(METHODS.keys()),
            variable=self.method_var,
            width=280,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self._on_method_changed,
        )
        self.method_dropdown.place(relx=0.08, rely=0.28, anchor="w")

        self.constraint_label = ctk.CTkLabel(
            self,
            text=f"n: {METHODS[self.method_var.get()]['n_constraint']}",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65"),
        )
        self.constraint_label.place(relx=0.08, rely=0.34, anchor="w")

    def _build_inputs(self) -> None:
        """Input fields for f(x), a, b, and n."""
        # ── f(x) ──────────────────────────────────────────────────────
        self.function_label = ctk.CTkLabel(
            self,
            text="f(x):",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.function_label.place(relx=0.08, rely=0.42, anchor="w")

        self.function_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.function_frame.place(relx=0.08, rely=0.49, anchor="w", relwidth=0.84)

        self.function_entry = ctk.CTkEntry(
            self.function_frame,
            placeholder_text="Ej: x**2 + sin(x)",
            height=42,
            font=ctk.CTkFont(size=15, family="Consolas"),
        )
        self.function_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.keyboard_button = ctk.CTkButton(
            self.function_frame,
            text="⌨️",
            width=42,
            height=42,
            corner_radius=10,
            fg_color=("#6B4C9A", "#4B2C7A"),
            hover_color=("#7B5CAA", "#5B3C8A"),
            command=self._open_keyboard,
        )
        self.keyboard_button.pack(side="left")

        # ── Interval and n (in one row) ────────────────────────────────
        self.params_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.params_frame.place(relx=0.08, rely=0.60, anchor="w", relwidth=0.84)

        for label_text, placeholder in [("a (límite inferior)", "0"), ("b (límite superior)", "1"), ("n (subdivisiones)", "100")]:
            col = ctk.CTkFrame(self.params_frame, fg_color="transparent")
            col.pack(side="left", expand=True, fill="x", padx=(0, 12))

            ctk.CTkLabel(col, text=label_text, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
            entry = ctk.CTkEntry(col, placeholder_text=placeholder, height=40, font=ctk.CTkFont(size=14, family="Consolas"))
            entry.pack(fill="x")

            # Keep references
            if "inferior" in label_text:
                self.a_entry = entry
            elif "superior" in label_text:
                self.b_entry = entry
            else:
                self.n_entry = entry

    def _build_action_buttons(self) -> None:
        """Primary action buttons: Calculate and Graph."""
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.place(relx=0.5, rely=0.75, anchor="center")
        
        self.calculate_button = ctk.CTkButton(
            self.buttons_frame,
            text="Calcular Integral",
            width=200,
            height=48,
            corner_radius=24,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=("#3B8ED5", "#1F6AA5"),
            hover_color=("#4A9FE8", "#2A7AB5"),
            command=self._calculate,
        )
        self.calculate_button.pack(side="left", padx=10)

        self.graph_button = ctk.CTkButton(
            self.buttons_frame,
            text="Gráfica 📈",
            width=160,
            height=48,
            corner_radius=24,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=("#10B981", "#059669"),
            hover_color=("#34D399", "#10B981"),
            command=self._graph_function,
        )
        self.graph_button.pack(side="left", padx=10)

    def _build_result_panel(self) -> None:
        """Panel that displays the numerical result or error messages."""
        self.result_frame = ctk.CTkFrame(self, corner_radius=16)
        self.result_frame.place(relx=0.5, rely=0.88, anchor="center", relwidth=0.84, relheight=0.14)

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="El resultado aparecerá aquí",
            font=ctk.CTkFont(size=16, family="Segoe UI"),
            text_color=("gray45", "gray65"),
        )
        self.result_label.place(relx=0.5, rely=0.5, anchor="center")

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_method_changed(self, selected_method: str) -> None:
        """Update the n-constraint hint when the user picks a different method."""
        constraint = METHODS[selected_method]["n_constraint"]
        self.constraint_label.configure(text=f"n: {constraint}")
        
        if selected_method == "Cuadratura de Gauss (2 puntos)":
            self.n_entry.delete(0, "end")
            self.n_entry.insert(0, "- - -")
            self.n_entry.configure(state="disabled")
        else:
            self.n_entry.configure(state="normal")
            if self.n_entry.get() == "- - -":
                self.n_entry.delete(0, "end")
                self.n_entry.insert(0, METHODS[selected_method]["n_default"])

    def _open_keyboard(self) -> None:
        """Open the virtual math keyboard targeting the function entry."""
        from ui.keyboard_view import KeyboardView
        KeyboardView(parent=self, input_widget=self.function_entry)

    def _calculate(self) -> None:
        """Read inputs, run the selected integration method, and display the result."""
        try:
            f = self._parse_function(self.function_entry.get().strip())
            a = self._parse_float(self.a_entry.get().strip(), "a")
            b = self._parse_float(self.b_entry.get().strip(), "b")

            if a >= b:
                raise ValueError("El límite inferior a debe ser menor que b.")

            method_name = self.method_var.get()
            method_config = METHODS[method_name]
            integrate = method_config["function"]
            
            if method_name == "Cuadratura de Gauss (2 puntos)":
                result = integrate(f, a, b)
            else:
                n = self._parse_int(self.n_entry.get().strip(), "n")
                result = integrate(f, a, b, n)

            self._show_result(result)

        except (ValueError, SympifyError, ZeroDivisionError, TypeError) as error:
            self._show_error(str(error))

    def _graph_function(self) -> None:
        """Parse inputs and open the graphing window."""
        try:
            expr_str = self.function_entry.get().strip()
            f = self._parse_function(expr_str)
            a = self._parse_float(self.a_entry.get().strip(), "a")
            b = self._parse_float(self.b_entry.get().strip(), "b")

            if a >= b:
                raise ValueError("El límite inferior a debe ser menor que b.")

            plot_integral_window(self, f, a, b, expr_str)

        except (ValueError, SympifyError, ZeroDivisionError, TypeError) as error:
            self._show_error(str(error))

    # ------------------------------------------------------------------
    # Input parsing helpers
    # ------------------------------------------------------------------

    def _parse_function(self, expression: str):
        """Parse a user-typed string into a callable f(x) using SymPy.

        Args:
            expression: Math expression as a string, e.g. 'x**2 + sin(x)'.

        Returns:
            A Python callable that evaluates the expression for a given x.

        Raises:
            ValueError: If the expression is empty or cannot be parsed.
        """
        if not expression:
            raise ValueError("Por favor ingresa una función f(x).")

        x = symbols("x")
        try:
            symbolic_expr = sympify(expression)
        except SympifyError:
            raise ValueError(f"No se pudo interpretar la función: '{expression}'")

        return lambdify(x, symbolic_expr, modules=["math"])

    def _parse_float(self, value: str, field_name: str) -> float:
        """Convert a string to float, raising a descriptive error on failure."""
        if not value:
            raise ValueError(f"El campo '{field_name}' está vacío.")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"'{value}' no es un número válido para '{field_name}'.")

    def _parse_int(self, value: str, field_name: str) -> int:
        """Convert a string to int, raising a descriptive error on failure."""
        if not value:
            raise ValueError(f"El campo '{field_name}' está vacío.")
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"'{value}' no es un entero válido para '{field_name}'.")

    # ------------------------------------------------------------------
    # Result display helpers
    # ------------------------------------------------------------------

    def _show_result(self, value: float) -> None:
        """Display the integration result in the result panel."""
        method_name = self.method_var.get()
        text = f"∫f(x)dx ≈  {value:.10f}     [{method_name}]"
        self.result_label.configure(
            text=text,
            text_color=("#1A7A3C", "#4ADE80"),
            font=ctk.CTkFont(size=16, weight="bold", family="Consolas"),
        )

    def _show_error(self, message: str) -> None:
        """Display an error message in the result panel."""
        self.result_label.configure(
            text=f"⚠ {message}",
            text_color=("#B91C1C", "#F87171"),
            font=ctk.CTkFont(size=13, family="Segoe UI"),
        )