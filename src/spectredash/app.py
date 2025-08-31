import seaborn as sns
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from spectredash.getduck import duckdb_table
from spectredash.tables import table_overview, table_pointer
from spectredash.utils import filter_and_sort_versions
import emoji




from pathlib import Path
import duckdb
import pandas as pd


def datasets():
    df = duckdb_table(table="pointers")
    tables = df["table"].unique().tolist()
    return tables


df = sns.load_dataset('penguins')  # Replace with your dataset name if needed


# The contents of the first 'page' is a navset with two 'panels'.
page1 = ui.navset_card_underline(
    ui.nav_panel(ui.h2(f"{emoji.emojize(':water_pistol:')} About the app", class_="m-0"),
        ui.row(
            ui.column(
                5,
                ui.div(
                    ui.p(
                        "Spectre silently infiltrates the OddJob repository, extracting validation results "
                        "and decoding them into sleek visual intel. Validation results and pointer data create "
                        "a rich meta data for a complete audit trail."
                    ),
                    ui.p("The table on the right side gives an overview of the most recent validation runs. Pick a table name (and version) and SpectreApp visualize key insights"),
                    #ui.hr(),
                    ui.p("Furthermore, this app includes:"),
                    ui.tags.ul(
                        ui.tags.li(ui.strong("Overview:"), " An overview based on the pointer file."),
                        ui.tags.li(ui.strong("Validation:"), " The validation report created with Octopussy."),
                        ui.tags.li(ui.strong("Variable Matrix:"), " Displays which variables the data includes."),
                        ui.tags.li(ui.strong("Class Matrix:"), " Depicts which classes the data includes."),
                        ui.tags.li(ui.strong("Label Matrix:"), " Shows which labels the data includes.")
                        ),
                        ui.p(f"Create with {emoji.emojize(':red_heart:')}, shiny, and ",
                        ui.tags.img(src="octo.png", height="32px", class_="me-2")
                        )
                ),
            ),
            ui.column(
                7,
                ui.h4("Select the intel for:", class_="text-muted small"),
                ui.row(
                    ui.column(6,
                    ui.input_select( "first_choice", "Pick your table:", choices=datasets(),  selected=datasets()[0] if datasets() else None),
                    #ui.input_select("first_choice", "Pick your table:", choices=datasets()),
                    ),
                    ui.column(6,
                    ui.output_ui("dependent_select"),
                    #ui.input_select("var", "Version (optional)", choices=["bill_length_mm", "body_mass_g"])
                    ),
                    ui.p("Monitoring data made simple with spectre.", class_="text-muted small")
                    ),
                ui.hr(),
                ui.output_ui("table_html")
            )
        )
    )
)




page2 = ui.navset_card_underline(
    ui.nav_panel(ui.h2(f"{emoji.emojize(':brain:')} Overview of the run", class_="m-0"), 
    ui.output_ui("table_html2")
    #ui.output_plot("hist")
    ),
    footer=ui.input_select(
        "vari", "Select variable", choices=["bill_length_mm", "body_mass_g"]
    )
)


app_ui = ui.page_navbar(
    ui.nav_panel("About", page1),
    ui.nav_panel("Overview", page2),
    title = ui.a(
        ui.span(ui.img(src="logo.png", height="60px", class_="me-2"), 
        "SpectreApp"),
    href="/",  # Replace with your actual app URL path if needed
    class_="text-decoration-none d-flex align-items-center text-body"
),
    footer = ui.p(ui.tags.a("🎩 Visit the OddJob Repository", href="https://gitlab.lrz.de/edgar-treischl/OddJob", target="_blank")
)
)


def app_server(input: Inputs, output: Outputs, session: Session):

    @output
    @render.ui
    def dependent_select():
        choice = input.first_choice()
        if not choice:
            return ui.TagList()  # no choices yet

        filtered_df = filter_and_sort_versions(choice)
        versions = filtered_df['version'].astype(str).tolist()  # convert Series to list of strings

        if not versions:
            return ui.TagList(ui.h5("No versions available"))

        return ui.input_select("second_choice", "Optional: Pick an older version", choices=versions)


    @render.plot
    def hist():
        p = sns.histplot(df, x=input.vari(), facecolor="#007bc2", edgecolor="white")
        return p.set(xlabel=None)

    @render.data_frame
    def data():
       #return df[["species", "island", input.var()]]
        df = duckdb_table(table = "pointers")
        return df


    @output()
    @render.ui
    def table_html():
        df = duckdb_table(table = "pointers")
        # Generate HTML for styled table
        html = table_overview(df)
        return html

    @output()
    @render.ui
    def table_html2():
        choice = input.first_choice()
        #version = input.dependent_select()
        version = input.second_choice()

        if not choice:
            return ui.div("Please select a dataset first.")
        if not version:
            return ui.div("Please select a version first.")

        html = table_pointer(choice, version)
        return html

www_dir = Path(__file__).parent / "www"
app = App(app_ui, app_server, static_assets=www_dir)

