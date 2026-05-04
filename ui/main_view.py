"""Vista principal - Punto de entrada después de la pantalla de inicio.

Actualmente redirige directamente a la vista de Integración.
Se pueden agregar herramientas adicionales aquí como tarjetas de navegación en el futuro.
"""

import customtkinter as ctk
from ui.base_view import BaseView


class MainView(BaseView):
    """Vista del concentrador principal con tarjetas de navegación a cada herramienta."""

    def __init__(self):
        super().__init__()

        self.title_label = ctk.CTkLabel(
            self,
            text="Selecciona una herramienta",
            font=ctk.CTkFont(size=28, weight="bold", family="Segoe UI"),
        )
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")

        self.integration_button = ctk.CTkButton(
            self,
            text="📐  Integración Numérica",
            width=280,
            height=60,
            corner_radius=20,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#3B8ED5", "#1F6AA5"),
            hover_color=("#4A9FE8", "#2A7AB5"),
            command=self._go_to_integration,
        )
        self.integration_button.place(relx=0.5, rely=0.5, anchor="center")

    def _go_to_integration(self) -> None:
        """Navegar a la vista de integración numérica."""
        from ui.integration_view import IntegrationView
        self.go_to_view(IntegrationView)