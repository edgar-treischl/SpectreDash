import seaborn as sns
from shiny import App, render, ui
from spectredash.duckdb_table import duckdb_table
from spectredash.tables import table_overview



df = sns.load_dataset('penguins')  # Replace with your dataset name if needed


# The contents of the first 'page' is a navset with two 'panels'.
page1 = ui.navset_card_underline(
    ui.nav_panel("Plot", 
    ui.row(
            ui.column(6, ui.input_select("varA", "Select Data", choices=["mtcars", "iris"])),
            ui.column(6, ui.input_select("varB", "Select variable", choices=["bill_length_mm", "body_mass_g"]))
        ),
    ui.output_ui("table_html")),
    #ui.output_plot("hist")),
    ui.nav_panel("Table", ui.output_data_frame("data")),
    footer=ui.input_select(
        "var", "Select variable", choices=["bill_length_mm", "body_mass_g"]
    ),
    title="Penguins data",
)

page2 = ui.navset_card_underline(
    ui.nav_panel("About", ui.output_plot("histi")),
    ui.nav_panel("Data", ui.output_data_frame("datai")),
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


def server(input, output, session):
    @render.plot
    def histi():
        p = sns.histplot(df, x=input.var(), facecolor="#007bc2", edgecolor="white")
        return p.set(xlabel=None)


    @render.plot
    def hist():
        p = sns.histplot(df, x=input.var(), facecolor="#007bc2", edgecolor="white")
        return p.set(xlabel=None)

    @render.data_frame
    def datai():
        return df[["species", "island", input.var()]]

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


app = App(app_ui, server)