"""Main entry point for Integrator App."""
import customtkinter as ctk
from ui.base_view import BaseView


def main():
    """Launch the application."""
    app = BaseView()
    app.mainloop()


if __name__ == "__main__":
    main()