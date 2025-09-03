# overview.py
from shiny import module, ui, render, reactive
import emoji
from spectredash.tables import table_pointer
from spectredash.getduck import duckdb_table

from spectredash.utils import shared_first_choice, shared_second_choice


@module.ui
def overview_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.div(
                {"class": "mb-3"}, 
                ui.h4(f"{emoji.emojize(':clipboard:')} Overview", class_="m-0"),
                ui.p(
                    "A quick overview about the data.",
                    class_="text-muted small mb-0"
                )
            ),            
            ui.output_ui("table_html2"),
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

