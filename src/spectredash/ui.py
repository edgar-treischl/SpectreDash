# Import data from shared.py
# 
from shiny import App, render, ui

def icon_html(icon_name):
    return ui.HTML(f'<i class="fa {icon_name}"></i>')


page1 = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("hist")),
    ui.nav_panel("Table", ui.output_data_frame("data")),
    footer=ui.input_select(
        "var", "Select variable", choices=["bill_length_mm", "body_mass_g"]
    ),
    title="Penguins data",
)

app_ui = ui.page_navbar(
    # Include Font Awesome CDN
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css")
    ),
    #ui.nav_spacer(),  # Push the navbar items to the right
    ui.nav_panel("Page 1", page1, icon=ui.tags.i(class_="fas fa-thumbs-up")),
    ui.nav_panel("Page 2", "This is the second 'page'."),
    title="Shiny navigation components",
)