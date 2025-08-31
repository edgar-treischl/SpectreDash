import seaborn as sns
from shiny import App, render, ui
from spectredash.getduck import duckdb_table
from spectredash.tables import table_overview



df = sns.load_dataset('penguins')  # Replace with your dataset name if needed


# The contents of the first 'page' is a navset with two 'panels'.
page1 = ui.navset_card_underline(
    ui.nav_panel(
        ui.row(
            ui.column(
                5,
                ui.div(
                    ui.p(
                        "SpectreApp silently infiltrates the OddJob repository, extracting validation results "
                        "and decoding them into sleek visual intel. Validation results and pointer data create "
                        "a rich meta data for a complete audit trail."
                    ),
                    ui.p("The next table gives an overview of the most recent validation runs:"),
                    ui.input_select("datax", "Select Data", choices=["mtcars", "iris"]),
                    ui.input_select("var", "Select variable", choices=["bill_length_mm", "body_mass_g"])
                    #ui.hr(),
                ),
            ),
            ui.column(
                7,
                ui.output_ui("table_html")
            ),
        )
    ),
    title="Data Pointers"
)




page2 = ui.navset_card_underline(
    ui.nav_panel("About", ui.output_plot("hist")),
    footer=ui.input_select(
        "vari", "Select variable", choices=["bill_length_mm", "body_mass_g"]
    ),
    title="Penguins data",
)

app_ui = ui.page_navbar(
    #ui.nav_spacer(),
    ui.nav_panel("Bla", page1),
    ui.nav_panel("More", page2),
    title="Spectr",
)


def app_server(input, output, session):

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


app = App(app_ui, app_server)