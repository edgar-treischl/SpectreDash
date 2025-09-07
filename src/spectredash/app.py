# ---- Imports ----
from shiny import App, Inputs, Outputs, Session, ui
from pathlib import Path
import emoji


from spectredash.moduleAbout import about_ui, about_server
from spectredash.moduleOverview import overview_ui, overview_server
from spectredash.moduleValidation import validation_ui, validation_server
from spectredash.moduleVariables import variables_ui, variables_server
from spectredash.moduleClass import class_ui, class_server
from spectredash.moduleLabels import labels_ui, labels_server
from spectredash.moduleDiff import diff_ui, diff_server
from spectredash.modulePipe import pipe_ui, pipe_server


# ---- App UI ----
app_ui = ui.page_navbar(
    ui.nav_panel("About", about_ui("about")),
    ui.nav_panel("Overview", overview_ui("overview")),
    ui.nav_panel("Pipe", pipe_ui("pipe")),
    ui.nav_panel("Validation", validation_ui("validation")),
    ui.nav_panel("Variables", variables_ui("variables")),
    ui.nav_panel("Classes", class_ui("class")),
    ui.nav_panel("Labels", labels_ui("labels")),
    ui.nav_panel("Diff", diff_ui("diff")),
    title=ui.a(
        ui.span(ui.img(src="logo.png", height="60px", class_="me-2"), "Spectre"),
        href="/",
        class_="text-decoration-none d-flex align-items-center text-body",
    ),
    footer=ui.tags.footer(
        {"style": "text-align: center; padding: 10px; font-size: 0.9em; color: #666;"},
        ui.HTML("Created with "),
        ui.tags.a(
            emoji.emojize(":top_hat:"),
            href="https://gitlab.lrz.de/edgar-treischl/OddJob",
            target="_blank",
            style="color: #666; text-decoration: underline;",
        ),
        ui.HTML(", shiny, and "),
        ui.tags.a(
            emoji.emojize(":octopus:"),
            href="https://gitlab.lrz.de/edgar-treischl/octopussy",
            target="_blank",
            style="color: #666; text-decoration: underline;",
        ),
        ui.HTML(" | By: "),
        ui.tags.a(
            "Edgar Treischl",
            href="https://edgar-treischl.de",
            target="_blank",
            style="color: #666; text-decoration: underline;",
        )
        # ui.HTML(" | "),
    )
)


# ---- App Server ----
def app_server(input: Inputs, output: Outputs, session: Session):
    about_server("about")
    overview_server("overview")
    pipe_server("pipe")
    validation_server("validation")
    variables_server("variables")
    class_server("class")
    labels_server("labels")
    diff_server("diff")


www_dir = Path(__file__).parent / "www"
app = App(app_ui, app_server, static_assets=www_dir)
