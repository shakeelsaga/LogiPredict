from app import create_app

# I'm calling the factory function I built in app/__init__.py.
app = create_app()

if __name__ == '__main__':
    # I'm running the app here. I've set debug=True so the server will auto-reload
    # whenever I make code changes.
    app.run(debug=True)