"""Main entry point for Integrator App."""
from ui.home_view import HomeView


def main():
    """Launch the application."""
    app = HomeView()
    app.mainloop()


if __name__ == "__main__":
    main()