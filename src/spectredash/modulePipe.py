from shiny import module, reactive, render, ui
import emoji
from plotnine import ggplot
from spectredash.plots import plot_pipe
from spectredash.utils import shared_first_choice


@module.ui
def pipe_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.div(
                {"class": "mb-3"}, 
                ui.h4(f"{emoji.emojize(':label:')} Pipe", class_="m-0"),
                ui.p(
                    "What does the validation pipe test?",
                    class_="text-muted small mb-0"
                )
            ),
            ui.output_ui("pipe_plot_ui")
        )
    )


@module.server
def pipe_server(input, output, session):
    plot_state = reactive.Value({"success": True, "error": None, "plot": None})

    @reactive.Calc
    def pipe_plot():
        user_table = shared_first_choice.get()

        if not user_table:
            return {"success": False, "error": "No dataset selected.", "plot": None}

        try:
            plot_obj = plot_pipe()
            return {"success": True, "plot": plot_obj, "error": None}
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating plot for '{user_table}': {str(e)}",
                "plot": None
            }

    @reactive.Effect
    def update_state():
        plot_state.set(pipe_plot())

    @output
    @render.ui
    def pipe_plot_ui():
        result = plot_state.get()
        if result["success"] and isinstance(result["plot"], ggplot):
            return ui.div(
                # The output_plot ID here must be unique and matched by the render.plot below
                ui.output_plot("label_dot_plot", width="100%", height="600px")
            )
        else:
            return ui.div(
                ui.tags.i(class_="fas fa-exclamation-circle text-warning fa-4x mb-3"),
                ui.h4("Plot Not Available", class_="text-danger"),
                ui.p(result["error"], class_="text-muted text-center"),
                class_="d-flex flex-column justify-content-center align-items-center",
                style="min-height: 400px; background-color: #f8f9fa;"
            )

    @output
    @render.plot(alt="Pipe Dot Plot")
    def label_dot_plot():
        result = plot_state.get()
        return result["plot"] if result["success"] else None
