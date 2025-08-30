# src/spectredash/about.py
import shiny
from shiny import ui

def about_ui():
    return ui.div(
        "SpectreApp silently infiltrates the OddJob repository, extracting validation results and decoding them into sleek visual intel.",
        class_="container"
    )

def about_server():
    pass
