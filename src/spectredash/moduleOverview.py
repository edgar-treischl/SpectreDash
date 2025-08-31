# overview.py
from shiny import module, ui, render, reactive
import emoji
from spectredash.tables import table_pointer
from spectredash.getduck import duckdb_table

from spectredash.state import shared_first_choice, shared_second_choice


@module.ui
def overview_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.h2(f"{emoji.emojize(':brain:')} Overview of the run", class_="m-0"),
            ui.output_ui("table_html2"),
            # ui.output_plot("hist"),  # optional additional outputs
        ),
        footer=ui.input_select(
            "vari",
            "Select variable",
            choices=["bill_length_mm", "body_mass_g"]
        )
    )





@module.server
def overview_server(input, output, session):
    
    @output
    @render.ui
    def table_html2():
        choice = shared_first_choice.get()
        version = shared_second_choice.get()

        if not choice or not version:
            return ui.div("Please select both a table and a version.")

        return table_pointer(choice, version)

