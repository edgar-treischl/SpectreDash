from shiny import module, reactive, render, ui
import emoji
from plotnine import ggplot
from spectredash.plots import plot_TypeMatrixWeb
from spectredash.utils import shared_first_choice


@module.ui
def class_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.h4(f"{emoji.emojize(':school:')} Classes", class_="m-0"),
            ui.row(
                ui.column(
                    4,
                    ui.card(
                        ui.p("This panel shows the distribution of classes (levels) within factor-like variables across dataset versions."),
                        ui.tags.ul(
                            ui.tags.li("Each facet or section represents one categorical variable."),
                            ui.tags.li("You can track if levels have changed, disappeared, or appeared."),
                            ui.tags.li("Useful for identifying category drift or inconsistent encoding."),
                        ),
                        ui.p({"class": "text-muted small"}, "Look for unexpected class changes or missing categories over time.")
                    )
                ),
                ui.column(
                    8,
                    ui.card(
                        ui.div(
                            {"style": "overflow-x: auto"},
                            ui.output_ui("class_plot_ui")
                        )
                    )
                )
            )
        )
    )


@module.server
def class_server(input, output, session):
    plot_state = reactive.Value({"success": True, "error": None, "plot": None})

    @reactive.Calc
    def class_plot():
        user_table = shared_first_choice.get()

        if not user_table:
            return {"success": False, "error": "No dataset selected.", "plot": None}

        try:
            plot_obj = plot_TypeMatrixWeb(table=user_table)
            return {"success": True, "plot": plot_obj, "error": None}
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating plot for '{user_table}': {str(e)}",
                "plot": None
            }

    @reactive.Effect
    def update_state():
        plot_state.set(class_plot())

    @output
    @render.ui
    def class_plot_ui():
        result = plot_state.get()
        if result["success"] and isinstance(result["plot"], ggplot):
            return ui.div(
                # The output_plot ID here must be unique and matched by the render.plot below
                ui.output_plot("class_matrix_plot", width="100%", height="600px")
            )
        else:
            return ui.div(
                {"class": "d-flex flex-column justify-content-center align-items-center",
                 "style": "min-height: 400px; background-color: #f8f9fa;"},
                ui.tags.i(class_="fas fa-exclamation-circle text-warning fa-4x mb-3"),
                ui.h4("Plot Not Available", class_="text-danger"),
                ui.p(result["error"], class_="text-muted text-center"),
            )

    @output
    @render.plot(alt="Class Matrix")
    def class_matrix_plot():
        result = plot_state.get()
        return result["plot"] if result["success"] else None
