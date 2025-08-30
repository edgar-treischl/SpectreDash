import shiny
from shiny import ui, reactive, output, render
import duckdb
import pandas as pd

def about_ui(id):
    """
    About user interface for the Shiny app.

    Args:
    - id (str): The namespace ID for the module.
    
    Returns:
    - shiny.ui: The UI for the About section.
    """
    ns = shiny.NS(id)
    
    return ui.layout_column_wrap(
        width="100%",
        fill=False,
        children=[
            ui.card(
                class_="shadow-sm",
                children=[
                    ui.card_header(
                        class_="bg-light",
                        children=[ui.h2("About", class_="m-0")]
                    ),
                    ui.card_body(
                        children=[
                            ui.p(
                                "SpectreApp silently infiltrates the OddJob repository, extracting validation results and decoding them into sleek visual intel. "
                                "Validation results and pointer data create a rich meta data for a complete audit trail."
                            ),
                            ui.p("The next table gives an overview of the most recent validation runs:"),
                            ui.hr(),
                            ui.ui_output(ns("overview_table")),
                            ui.p("Furthermore, this app includes:"),
                            ui.tags.ul(
                                children=[
                                    ui.tags.li(ui.strong("Overview:"), " An overview based on the pointer file."),
                                    ui.tags.li(ui.strong("Validation:"), " The validation report created with Octopussy."),
                                    ui.tags.li(ui.strong("Variable Matrix:"), " Displays which variables the data includes."),
                                    ui.tags.li(ui.strong("Class Matrix:"), " Depicts which classes the data includes."),
                                    ui.tags.li(ui.strong("Label Matrix:"), " Shows which labels the data includes.")
                                ]
                            ),
                            ui.hr(),
                            ui.p(
                                "Created with ",
                                ui.icon("heart", style="color: red;"),
                                ", shiny, and ",
                                ui.img(src="images/octo.png", height="32px", class_="me-2")
                            )
                        ]
                    )
                ]
            )
        ]
    )



def about_server(id):
    """
    About server logic for the Shiny app.

    Args:
    - id (str): The namespace ID for the module.
    """
    @shiny.module_server(id)
    def server(input, output, session):
        
        # Load global data (using the same logic as the DuckDB interaction)
        def duckdb_table(table):
            db_path = "data/meta.duckdb"  # Path to your DuckDB file
            con = duckdb.connect(db_path, read_only=True)
            try:
                # Fetch the table from DuckDB
                query = f"SELECT * FROM {table}"
                return con.execute(query).fetchdf()
            finally:
                con.close()

        global_data = duckdb_table("global_data")

        # Render the overview table dynamically
        @output
        def overview_table():
            try:
                table_obj = table_overview(data=global_data)
                return table_obj
            except Exception as e:
                return ui.div(
                    class_="text-danger",
                    children=[f"Unable to generate summary table:<br><em>{str(e)}</em>"]
                )

def table_overview(data):
    """
    A placeholder function to generate an overview table.
    
    Replace with actual logic to render a table overview.
    
    Args:
    - data (pd.DataFrame): The data to summarize.
    
    Returns:
    - shiny.ui: The UI representation of the table.
    """
    # Replace this with your own table rendering logic (e.g., using a pandas DataFrame to display the table)
    # Here's a basic placeholder:
    return ui.table(data)
