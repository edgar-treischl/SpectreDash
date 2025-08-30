# Import data from shared.py
# 
from shiny import App, render, ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "var", "Select variable", choices=["bill_length_mm", "body_mass_g"]
        ),
        ui.input_switch("species", "Group by species", value=True),
        ui.input_switch("show_rug", "Show Rug", value=True),
    ),
    ui.output_plot("hist"),
    title="Hello sidebar!",
)