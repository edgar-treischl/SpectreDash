# src/spectredash/about.py

from shiny import module, render, ui, reactive
import emoji
from spectredash.utils import filter_and_sort_versions, datasets
from spectredash.getduck import duckdb_table
from spectredash.tables import table_pointer, table_overview

from spectredash.utils import shared_first_choice, shared_second_choice

@module.ui
def about_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.h4(f"{emoji.emojize(':water_pistol:')} About the app", class_="m-0"),
            ui.row(
                ui.column(
                    6,
                    ui.div(
                        ui.p(
                            "Spectre silently infiltrates the OddJob repository, extracting validation results "
                            "and decoding them into sleek visual intel. Validation results and pointer data create "
                            "a rich meta data for a complete audit trail."
                        ),
                        ui.p("The table on the right side gives an overview of the most recent validation runs. Pick a table name (and version) and SpectreApp visualizes key insights."),
                        ui.p("Furthermore, this app includes:"),
                        ui.tags.ul(
                            ui.tags.li(ui.strong("Overview:"), " An overview based on the pointer file."),
                            ui.tags.li(ui.strong("Validation:"), " The validation report created with Octopussy."),
                            ui.tags.li(ui.strong("Variable Matrix:"), " Displays which variables the data includes."),
                            ui.tags.li(ui.strong("Class Matrix:"), " Depicts which classes the data includes."),
                            ui.tags.li(ui.strong("Label Matrix:"), " Shows which labels the data includes."),
                        ),
                        ui.p(
                            f"Created with {emoji.emojize(':red_heart:')}, shiny, and {emoji.emojize(':octopus:')}."
                        )
                    ),
                ),
                ui.column(
                    6,
                    ui.h4("Select the intel for:", class_="text-muted small"),
                    ui.row(
                        ui.column(
                            6,
                            ui.input_select(
                                "first_choice",
                                "Data:",
                                choices=datasets(),
                                selected=datasets()[0] if datasets() else None
                            )
                        ),
                        ui.column(
                            6,
                            ui.output_ui("dependent_select"),
                        ),
                        ui.p("Monitoring data made simple with Spectre.", class_="text-muted small")
                    ),
                    ui.br(),
                    #ui.hr(),
                    ui.output_ui("table_html")
                )
            )
        )
    )




@module.server
def about_server(input, output, session):
    
    @output
    @render.ui
    def dependent_select():
        choice = input.first_choice()
        if not choice:
            return ui.TagList()  # Return nothing if no choice

        filtered_df = filter_and_sort_versions(choice)
        versions = filtered_df['version'].astype(str).tolist()

        if not versions:
            return ui.TagList(ui.h5("No versions available"))

        return ui.input_select(
            "second_choice",
            "Optional: Pick a version",
            choices=versions
        )

    @output()
    @render.ui
    def table_html2():
        choice = input.first_choice()
        version = input.second_choice()

        if not choice:
            return ui.div("Please select a dataset first.")
        if not version:
            return ui.div("Please select a version first.")

        return table_pointer(choice, version)

    @output()
    @render.ui
    def table_html():
        df = duckdb_table(table="pointers")
        return table_overview(df)

    @reactive.Effect
    def _():
        choice = input.first_choice()
        if choice is not None:
            shared_first_choice.set(choice)
    
    @reactive.Effect
    def _():
        version = input.second_choice()
        if version is not None:
            shared_second_choice.set(version)



