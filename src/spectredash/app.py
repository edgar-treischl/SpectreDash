import seaborn as sns
from shiny import App, render, ui
from spectredash.getduck import duckdb_table
from spectredash.tables import table_overview
from pathlib import Path


df = sns.load_dataset('penguins')  # Replace with your dataset name if needed


# The contents of the first 'page' is a navset with two 'panels'.
page1 = ui.navset_card_underline(
    ui.nav_panel(
        "🔫 About",
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
                        ui.p("Created with ❤️, shiny, and ",
                        ui.tags.img(src="octo.png", height="32px", class_="me-2")
                        )
                ),
            ),
            ui.column(
                7,
                ui.h4("Select the intel for:", class_="text-muted small"),
                ui.row(
                    ui.column(6,
                    ui.input_select("datax", "Data", choices=["mtcars", "iris"])
                    ),
                    ui.column(6,
                    ui.input_select("var", "Version (optional)", choices=["bill_length_mm", "body_mass_g"])
                    ),
                    ui.p("Monitoring data made simple with spectre.", class_="text-muted small")
                    ),
                ui.hr(),
                ui.output_ui("table_html")
            ),
        )
    )
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
    ui.nav_panel("About", page1),
    ui.nav_panel("More", page2),
    title=ui.span(
        ui.img(src="logo.png", height="60px", class_="me-2"),
        "SpectreApp"
    ),
    footer = ui.p(ui.tags.a("🎩 Visit the OddJob Repository", href="https://gitlab.lrz.de/edgar-treischl/OddJob", target="_blank")
)
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

www_dir = Path(__file__).parent / "www"
app = App(app_ui, app_server, static_assets=www_dir)

