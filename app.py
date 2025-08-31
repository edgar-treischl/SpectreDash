from shiny import App, Inputs, Outputs, Session, render, ui

app_ui = ui.page_fluid(
    ui.input_select("first_choice", "Pick an option", choices=["fruits", "colors"]),
    ui.output_ui("dependent_select"),
)

def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.ui
    def dependent_select():
        choice = input.first_choice()
        if choice == "fruits":
            return ui.input_select("second_choice", "Pick a fruit", choices=["apple", "banana", "cherry"])
        elif choice == "colors":
            return ui.input_select("second_choice", "Pick a color", choices=["red", "green", "blue"])
        else:
            return ui.TagList()  # empty UI if no valid choice

app = App(app_ui, server)
