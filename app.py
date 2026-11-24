"""WSGI entry point for the container-safe ACEest delivery application."""

from aceest import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
