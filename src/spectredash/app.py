from spectredash.ui import app_ui
from spectredash.server import app_server
import shiny

# Expose the ASGI app as 'app' for Uvicorn to discover
app = shiny.App(app_ui, app_server)

# Run the app only when this script is executed directly (not when imported)
if __name__ == "__main__":
    app.run()
